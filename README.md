# Thyroid Disease Detection
This repository contains a data science project aiming to predict the risk of thyroid disease in patients. The project follows a classical machine learning workflow, including data exploration, cleaning, feature engineering, model building, and testing.

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/thyroid-disease-prediction.git
    cd thyroid-disease-prediction
    ```

2. Create a virtual conda environment using terminal:

    ```bash
    conda create -p venv python=3.8 -y
    
    conda activate venv/
    ```

3. Install dependencies (if any):

    ```bash
    pip install -r requirements.txt
    ```

4. Create .env file to save all environment variables:

 In the terminal window execute the following window
    
    ```bash
    touch .env
    ```

    Open the .env you created and add the MongoDB connection string

    ```bash
    MONGO_DB_URL=<Enter your connection string>
    ```

5. Run the entire source code in the terminal using:

    ```bash
    python main.py
    ```



## Contributing

Contributions are welcome! If you have suggestions for improvement, please open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
