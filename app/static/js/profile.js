const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const selectedCoursesDiv = document.getElementById('selected-courses');
let selectedCourses = [];


// Initialize selectedCourses array and checkboxes with existing course history
document.addEventListener('DOMContentLoaded', function() {
    checkboxes.forEach(checkbox => {
        takenCourses.forEach(takenCourse => {
            if (checkbox.name === takenCourse.course.title) {
                checkbox.checked = true;
                const label = checkbox.parentElement;
                label.classList.add('selected');
            }
        });
    });
});

// // Initializes selectedCourses array and checkboxes with existing course history
// document.querySelectorAll('.added-course').forEach(addedCourse => {
//     const courseName = addedCourse.innerHTML.trim();

//     // Successfully initializes selectedCourses array and checkboxes if the rendered template data
//     // matches an existing checkbox value
//     checkboxes.forEach(checkbox => {
//         if (checkbox.name === courseName) {
//             checkbox.checked = true;
//             label.classList.add('selected');
//             selectedCourses.push(courseName);
//         }
//     });
// });


// Highlights/Unhighlights selected checkbox on click
document.addEventListener('DOMContentLoaded', function() {
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', function() {
            const label = checkbox.parentElement;
            if (checkbox.checked) {
                label.classList.add('selected');
            } else {
                label.classList.remove('selected');
            }
        });
    });
});


// Adds selected checkbox item to selectedCourses array on click
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('click', function() {
        const courseName = this.name;
        if (this.checked) {
            if (!selectedCourses.includes(courseName)) {
                selectedCourses.push(courseName);
            }
        } else {
            const index = selectedCourses.indexOf(courseName);
            if (index !== -1) {
                selectedCourses.splice(index, 1);
            }
        }
        updateSelectedCourses();
    });
});


// Updates '.selected-courses' html with the selected courses sorted in ascending order
function updateSelectedCourses() {
    selectedCourses.sort();

    // Update the selectedCoursesDiv with the sorted courses
    selectedCoursesDiv.innerHTML = '';
    selectedCourses.forEach(course => {
        const courseElement = document.createElement('div');
        courseElement.classList.add('added-course')
        courseElement.textContent = course;
        selectedCoursesDiv.appendChild(courseElement);
    });
}


// Allows dropdown toggle
function toggleDropdown() {
    document.getElementById("dropdown-content").classList.toggle("show");
}


// Updates '.selected-year' with selected academic year
function selectYear(year) {
    document.getElementById("selected-year").innerText = year;
}


// Closes the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}


// Saves profile on click
function saveProfile() {
    const checkboxes = document.querySelectorAll('.checkbox-content input[type="checkbox"]:checked');
    const courseData = Array.from(checkboxes).map(checkbox => {
        const courseID = checkbox.value;
        const courseName = checkbox.parentNode.textContent.trim(); // Extract course name from label
        return { courseID, courseName, semesterTaken: 0 };
    });

    // Sends POST request to add selected courses to taken courses
    fetch('/dbapi/taken-courses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(courseData) // Send the array of course data
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to add taken courses.');
        }
        return response.json();
    })
    .then(data => {
        console.log('Taken courses added successfully:', data);
        // Optionally, perform any actions after successfully adding taken courses
    })
    .catch(error => {
        console.error('Error adding taken courses:', error);
        // Optionally, handle errors here
    });
    
    const selectedYear = document.getElementById('selected-year').textContent.trim();
    let studentYear;
    switch (selectedYear) {
        case '1st Year - Freshman':
            studentYear = 1;
            break;
        case '2nd Year - Sophomore':
            studentYear = 2;
            break;
        case '3rd Year - Junior':
            studentYear = 3;
            break;
        case '4th Year - Senior':
            studentYear = 4;
            break;
        default:
            studentYear = 0; // Handle the case for "5+ Years" or other options
            break;
    }

    function fetchUserIDAndUpdateStudentYear(studentYear) {
        fetch('/dbapi/get-user-id')
        .then(response => response.json())
        .then(data => {
            const userID = data.userID;
            console.log('User ID:', userID);
            
            // Send PUT request to update the user's studentYear in the database
            return fetch('/dbapi/users/semester/' + userID, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ studentYear }) // Send the updated studentYear
            });
        })
        .then(response => response.text())
        .then(data => {
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
    }

    fetchUserIDAndUpdateStudentYear(studentYear);
}


// Function to fetch the current academic year from the server
function fetchCurrentUserAcademicYear() {
    fetch('/dbapi/get-user-id')
    .then(response => response.json())
    .then(data => {
        const userID = data.userID;
        console.log('User ID:', userID);
        return fetch('/dbapi/users/year/' + userID, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json' // Remove the content type header
            }
        }); 
    })
    .then(response => response.text())
    .then(academicYear => {
        console.log('Academic Year:', academicYear);
        document.getElementById('selected-year').innerText = getAcademicYearText(parseInt(academicYear)); // Update the selected year dropdown
    })
    .catch(error => console.error('Error fetching current academic year:', error));
}

// Function to convert academic year integer to text
function getAcademicYearText(year) {
    switch (year) {
        case 1:
            return '1st Year - Freshman';
        case 2:
            return '2nd Year - Sophomore';
        case 3:
            return '3rd Year - Junior';
        case 4:
            return '4th Year - Senior';
        default:
            return '5+ Years';
    }
}

// Call the function to fetch the current academic year when the DOM content is loaded
document.addEventListener('DOMContentLoaded', fetchCurrentUserAcademicYear);

