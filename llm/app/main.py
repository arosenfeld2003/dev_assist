from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from dotenv import load_dotenv
import platform

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Get model ID from environment variable, with a fallback default
model_id = os.getenv("MODEL_ID", "deepseek-ai/deepseek-coder-1.3b-base") # smaller model
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # optional commercial LLM integration

def get_device():
    """
    Determine the best available device for running the model.
    Returns:
        str: 'cuda' for NVIDIA GPUs
             'mps' for Apple Silicon GPUs
             'cpu' if no GPU is available
    """
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"  # Apple Silicon GPU
    else:
        return "cpu"


# Define the expected structure of incoming requests
class CodeQuery(BaseModel):
    prompt: str  # The input prompt for code generation
    max_length: int = 1024  # Maximum length of generated response
    randomness: float = 0.7  # Controls randomness in generation (0.0 = deterministic, 1.0 = very random)
    use_openai: bool = False

@app.on_event("startup")
async def startup_event():
    """
    Initialize the model and tokenizer when the application starts.
    This is run once at startup, making the model globally available.
    """
    global model, tokenizer
    try:
        # Determine the appropriate device for model execution
        device = get_device()
        print(f"Using device: {device}")

        # Load the tokenizer for processing text input/output
        tokenizer = AutoTokenizer.from_pretrained(model_id)

        # Load the model with appropriate settings for the device
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            # Use float16 for GPU to save memory, float32 for CPU for compatibility
            torch_dtype=torch.float16 if device != "cpu" else torch.float32,
            device_map="auto"  # Automatically handle model placement on available devices
        )

        # Ensure model is on the correct device
        model.to(device)

    except Exception as e:
        print(f"Error loading model: {e}")
        raise


@app.get("/health")
async def health_check():
    """
    Endpoint to check the health of the service and get system information.
    Returns details about the runtime environment and hardware being used.
    """
    device = get_device()
    return {
        "status": "healthy",
        "device": device,
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "torch_version": torch.__version__,
        "openai_available": bool(os.getenv("OPENAI_API_KEY"))
    }


@app.post("/generate")
async def generate_code(query: CodeQuery):
    """
    Main endpoint for code generation.

    Args:
        query (CodeQuery): The input query containing prompt and generation parameters

    Returns:
        dict: Contains the generated code/response

    Raises:
        HTTPException: If any error occurs during generation
    """
    try:
        if query.use_openai and os.getenv("OPENAI_API_KEY"):
            # Use OpenAI
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    # TODO: Add system prompt
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": query.prompt}
                ],
                temperature=query.randomness,
                max_tokens=query.max_length
            )
            return {"response": response.choices[0].message.content}
        else:
            # Use local model
            device = get_device()

            # Convert input text to token IDs and move to appropriate device
            inputs = tokenizer(query.prompt, return_tensors="pt").to(device)

            # Generate response using local llm
            outputs = model.generate(
                **inputs,
                max_length=query.max_length,
                temperature=query.randomness,
                pad_token_id=tokenizer.eos_token_id  # Properly handle end of sequence
            )

        # Convert token IDs back to text
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))