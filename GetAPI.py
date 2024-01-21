from flask import Flask, request, jsonify
import requests
prediction_key = "27dea928805b4e6baf8b46e2854986b7"
endpoint = 'https://cvobjectdetector-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/060c28e6-5b5f-41cb-8426-5036e6cfa1b9/detect/iterations/Iteration1/image'

headers = {
    "Prediction-Key": prediction_key,
    "Content-Type": "application/octet-stream", 
}

app = Flask(__name__)

total_ribbons = 0
total_arrows = 0
total_stars = 0

prediction_threshold = 0.90

@app.route('/', methods=['GET'])
def detect_objects():
    global total_ribbons, total_arrows, total_stars

    try:
        # Provide the image file path
        image_path = "image1.jpeg"

        # Open the image file and read its contents
        with open(image_path, "rb") as image_file:
            # Replace this section with your actual prediction logic
            response = requests.post(endpoint, headers=headers, data=image_file.read())

        if response.status_code == 200:
            result = response.json()

            predictions = result.get("predictions", [])

            for obj in predictions:
                tag_name = obj["tagName"]
                probability = obj["probability"]

                # Check if the probability is above the threshold
                if probability >= prediction_threshold:
                    if tag_name == "Ribbon":
                        total_ribbons +=1
                    elif tag_name == "Arrow":
                        total_arrows +=1
                    elif tag_name == "Star":
                        total_stars +=1

            # Return the current counts for each product in JSON format
            response_json = {
                "Total Ribbons": total_ribbons,
                "Total Arrows": total_arrows,
                "Total Stars": total_stars
            }

            return jsonify(response_json)

        else:
            return jsonify({"Error": f"{response.status_code} - {response.text}"}), 500

    except Exception as e:
        return jsonify({"Error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

