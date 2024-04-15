const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const selectedCoursesDiv = document.getElementById('selected-courses');
let selectedCourses = [];


// Initializes selectedCourses array and checkboxes with existing course history
document.querySelectorAll('.added-course').forEach(addedCourse => {
    const courseName = addedCourse.innerHTML.trim();

    // Successfully initializes selectedCourses array and checkboxes if the rendered template data
    // matches an existing checkbox value
    checkboxes.forEach(checkbox => {
        if (checkbox.value === courseName) {
            checkbox.checked = true;
            label.classList.add('selected');
            selectedCourses.push(courseName);
        }
    });
});


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
        const courseName = this.value;
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
    const addedCourses = document.querySelector('.added-courses');
    const courseNames = Array.from(addedCourses).map(course => course.textContent.trim());
    const selectedYear = document.getElementById('selected-year').textContent().trim();

    // Sends PUT request to update course history
    fetch('/dbapi/taken-courses', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({courses: courseNames})
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error:', error));


    // Sends PUT request to update academic year
    fetch('/users', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({studentYear: selectedYear})
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
}