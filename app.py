import requests
import json
import gradio as gr

## BACKEND SIDE CODE
url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}
history = []


def generate_response(prompt):
    history.append(prompt)

    data = {
        "model": "perception",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        try:
            data = response.json()
            actual_response = data.get("response", "No response field found")
            return actual_response
        except json.JSONDecodeError:
            return "Error: Unable to parse JSON response"
    else:
        return f"Error: {response.status_code} - {response.text}"


## FRONTEND SIDE CODE

with gr.Blocks() as app:
    # Display logo at the top
    with gr.Row():
        gr.Image(value="image.png", width=80, show_label=False)  # Ensure "logo.png" is in the same directory

    gr.Interface(
        fn=generate_response,
        inputs=gr.Textbox(lines=4, placeholder="Enter your Prompt"),
        outputs="text"
    )

app.launch()