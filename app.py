from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run

from typing import Optional

# Importing constants and pipeline modules from the project
from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import VehicleData, VehicleDataClassifier
from src.pipline.training_pipeline import TrainPipeline

# Initialize FastAPI application
app = FastAPI()

# Mount the 'static' directory for serving static files (like CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 template engine for rendering HTML templates
templates = Jinja2Templates(directory='templates')

# Allow all origins for Cross-Origin Resource Sharing (CORS)
origins = ["*"]

# Configure middleware to handle CORS, allowing requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    """
    DataForm class to handle and process incoming form data.
    This class defines the vehicle-related attributes expected from the form.
    """
    def __init__(self, request: Request):
        self.request: Request = request
        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None

    @staticmethod
    def _parse_int(value: object) -> Optional[int]:
        if value is None:
            return None
        try:
            parsed_value = str(value).strip()
            return None if parsed_value == "" else int(parsed_value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _parse_float(value: object) -> Optional[float]:
        if value is None:
            return None
        try:
            parsed_value = str(value).strip()
            return None if parsed_value == "" else float(parsed_value)
        except (TypeError, ValueError):
            return None

    async def get_vehicle_data(self):
        """
        Method to retrieve and assign form data to class attributes.
        This method is asynchronous to handle form data fetching without blocking.
        """
        form = await self.request.form()
        self.Gender = self._parse_int(form.get("Gender"))
        self.Age = self._parse_int(form.get("Age"))
        self.Driving_License = self._parse_int(form.get("Driving_License"))
        self.Region_Code = self._parse_float(form.get("Region_Code"))
        self.Previously_Insured = self._parse_int(form.get("Previously_Insured"))
        self.Annual_Premium = self._parse_float(form.get("Annual_Premium"))
        self.Policy_Sales_Channel = self._parse_float(form.get("Policy_Sales_Channel"))
        self.Vintage = self._parse_int(form.get("Vintage"))
        self.Vehicle_Age_lt_1_Year = self._parse_int(form.get("Vehicle_Age_lt_1_Year"))
        self.Vehicle_Age_gt_2_Years = self._parse_int(form.get("Vehicle_Age_gt_2_Years"))
        self.Vehicle_Damage_Yes = self._parse_int(form.get("Vehicle_Damage_Yes"))

def _coerce_to_int(candidate: object) -> Optional[int]:
    """
    Safely convert prediction values into a plain integer.
    """
    if candidate is None:
        return None
    if isinstance(candidate, bool):
        return int(candidate)
    if isinstance(candidate, (int, float)):
        return int(candidate)
    if isinstance(candidate, str):
        try:
            return int(candidate)
        except ValueError:
            return None

    item_converter = getattr(candidate, "item", None)
    if callable(item_converter):
        try:
            return _coerce_to_int(item_converter())
        except Exception:
            return None

    return None


# Route to render the main page with the form
@app.get("/", tags=["authentication"])
async def index(request: Request):
    """
    Renders the main HTML form page for vehicle data input.
    """
    return templates.TemplateResponse(
            "vehicledata.html",{"request": request, "context": "Rendering"})

# Route to trigger the model training process
@app.get("/train")
async def trainRouteClient():
    """
    Endpoint to initiate the model training pipeline.
    """
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful!!!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")

# Route to handle form submission and make predictions
@app.post("/")
async def predictRouteClient(request: Request):
    """
    Endpoint to receive form data, process it, and make a prediction.
    """
    try:
        form = DataForm(request)
        await form.get_vehicle_data()
        
        vehicle_data = VehicleData(
                                Gender= form.Gender,
                                Age = form.Age,
                                Driving_License = form.Driving_License,
                                Region_Code = form.Region_Code,
                                Previously_Insured = form.Previously_Insured,
                                Annual_Premium = form.Annual_Premium,
                                Policy_Sales_Channel = form.Policy_Sales_Channel,
                                Vintage = form.Vintage,
                                Vehicle_Age_lt_1_Year = form.Vehicle_Age_lt_1_Year,
                                Vehicle_Age_gt_2_Years = form.Vehicle_Age_gt_2_Years,
                                Vehicle_Damage_Yes = form.Vehicle_Damage_Yes
                                )

        # Convert form data into a DataFrame for the model
        vehicle_df = vehicle_data.get_vehicle_input_data_frame()

        # Initialize the prediction pipeline
        model_predictor = VehicleDataClassifier()

        # Make a prediction and retrieve the result
        prediction_result = model_predictor.predict(dataframe=vehicle_df)

        if hasattr(prediction_result, "iloc"):
            value = (
                prediction_result.iloc[0, 0]
                if getattr(prediction_result, "ndim", 1) > 1
                else prediction_result.iloc[0]
            )
        else:
            value = prediction_result[0]

        # Ensure we have a plain Python scalar for comparison
        value = _coerce_to_int(value)

        # Interpret the prediction result as 'Response-Yes' or 'Response-No'
        status = "Response-Yes" if value == 1 else "Response-No"

        # Render the same HTML page with the prediction result
        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "context": status},
        )
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}

# Main entry point to start the FastAPI server
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)