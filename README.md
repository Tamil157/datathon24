# Project Structure

## Total Folders: 3

1. **Frontend - React.js**
   - **Components:** Located in `Frontend/src/components`, this folder contains all UI components of the project, each in separate JavaScript files. This segregation makes it easy to manipulate and edit components.
   - **Source:** `Frontend/src`
     - **App.js:** Contains all routes and Toast container.
     - **Index.js:** Renders App.js.

2. **Server (Node.js, Express.js)**
   - **Models:** The `server/models` folder contains the schema for the complaint section and register/login page, utilizing Mongoose.
   - **index.js:** Handles backend services. Includes Express.js, Axios, and CORS.

3. **PyServer (Flask)**
   - Contains all Jupyter Notebooks with their corresponding pickle files.
   - **model.py:** Flask file handling all API requests.
   - UI components for these models are present in `frontend/src/components/PyHome.js`.
   - **Datasets:** CSV files are pushed into the repository using Git LFS, which tracks files larger than 100 MB.
