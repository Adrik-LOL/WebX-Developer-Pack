const fs = require('fs');
const path = require('path');

// Get the path to the user's data directory (where your NW.js application files are stored)
const userDataPath = nw.App.dataPath;
let createProjectBtn;

// Define paths relative to the user's data directory
const projectsFolderPath = path.join(userDataPath, 'projects');
const recentProjectsFilePath = path.join(userDataPath, 'recentProjects.json');

// Function to populate recent projects list from JSON file
function populateRecentProjects() {
    fs.readFile(recentProjectsFilePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading recent projects file:', err);
            return;
        }
        const recentProjectsList = document.getElementById('recent-projects');
        recentProjectsList.innerHTML = '';
        const recentProjects = JSON.parse(data);
        recentProjects.forEach(project => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = project.path;
            a.textContent = project.name;
            li.appendChild(a);
            recentProjectsList.appendChild(li);
        });
    });
}

// Function to save recent projects to JSON file
function saveRecentProjects(recentProjects) {
    fs.writeFile(recentProjectsFilePath, JSON.stringify(recentProjects, null, 2), err => {
        if (err) {
            console.error('Error saving recent projects:', err);
        } else {
            console.log('Recent projects saved successfully.');
        }
    });
}

// Function to handle click event on "Create New Project" button
function handleCreateProjectClick() {
    // Remove event listener to prevent multiple attachments
    createProjectBtn.removeEventListener('click', handleCreateProjectClick);

    // Replace this with your logic to create a new project
    const projectName = prompt('Enter project name:');
    if (projectName) {
        const projectPath = path.join(projectsFolderPath, projectName);
        fs.mkdir(projectPath, { recursive: true }, err => {
            if (err) {
                console.error('Error creating project folder:', err);
            } else {
                const recentProjects = JSON.parse(fs.readFileSync(recentProjectsFilePath, 'utf8'));
                recentProjects.push({ name: projectName, path: projectPath });
                saveRecentProjects(recentProjects);
                alert(`Project "${projectName}" created successfully!`);
                populateRecentProjects();

                // Re-attach event listener after completing the action
                createProjectBtn.addEventListener('click', handleCreateProjectClick);
            }
        });
    }
}

// Populate recent projects on page load
document.addEventListener('DOMContentLoaded', () => {
    // Get reference to the "Create New Project" button
    createProjectBtn = document.getElementById('create-project-btn');

    // Add event listener for "Create New Project" button click
    createProjectBtn.addEventListener('click', handleCreateProjectClick);

    // Create projects folder if it doesn't exist
    fs.mkdir(projectsFolderPath, { recursive: true }, err => {
        if (err) {
            console.error('Error creating projects folder:', err);
        }
    });

    // Create recentProjects.json if it doesn't exist
    fs.access(recentProjectsFilePath, fs.constants.F_OK, err => {
        if (err) {
            console.log('Recent projects file not found. Creating new file.');
            saveRecentProjects([]);
        }
        populateRecentProjects();
    });
});