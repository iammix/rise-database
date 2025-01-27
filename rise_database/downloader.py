import os
import requests
import zipfile
from tqdm import tqdm

class RiseDatabase:
    def __init__(self):
        self.api_url = "https://rise-data-api-3ecdb0861d7f.herokuapp.com"

    def list_datasets(self):
        """List available datasets."""
        response = requests.get(f"{self.api_url}/list")
        if response.status_code == 200:
            return response.json()["files"]
        else:
            raise Exception("Failed to fetch dataset list.")

    def download_dataset(self, dataset_id, save_path="data"):
        """
        Download a specific dataset by its ID with a progress bar, unzip it, and delete the .zip file.

        Args:
            dataset_id (str): The ID of the dataset to download.
            save_path (str): The folder where the dataset will be saved and extracted.
        """
        # Create the folder if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        # Make the request to the API
        response = requests.get(f"{self.api_url}/download/{dataset_id}", stream=True)
        if response.status_code == 200:
            # Extract the dataset name from the headers
            dataset_name = response.headers.get(
                "Content-Disposition", "dataset.zip"
            ).split("filename=")[-1].strip('"')
            zip_file_path = os.path.join(save_path, dataset_name)

            # Get the total file size in bytes
            total_size = int(response.headers.get("content-length", 0))

            # Download the file with a progress bar
            with open(zip_file_path, "wb") as file, tqdm(
                desc=f"Downloading {dataset_name.split('.')[0]}",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    bar.update(len(chunk))

            print(f"\nDataset downloaded successfully: {zip_file_path}")

            # Unzip the file and delete the .zip file
            self._extract_and_cleanup(zip_file_path, save_path)
        else:
            raise Exception(
                f"Failed to download dataset. Status code: {response.status_code}"
            )

    def _extract_and_cleanup(self, zip_file_path, extract_to):
        """
        Extract a zip file and delete the zip file afterward.

        Args:
            zip_file_path (str): Path to the zip file.
            extract_to (str): Directory where the contents will be extracted.
        """
        print(f"Extracting {zip_file_path}...")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)


        # Delete the .zip file
        os.remove(zip_file_path)
        print(f"Extraction complete. Files extracted to: {extract_to}")
