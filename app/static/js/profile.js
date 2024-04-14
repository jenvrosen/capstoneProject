document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.checkbox-content input[type="checkbox"]');
    
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

const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const selectedCoursesDiv = document.getElementById('selected-courses');
let selectedCourses = [];

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

function updateSelectedCourses() {
    // Sort the selectedCourses array
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

function toggleDropdown() {
    document.getElementById("dropdown-content").classList.toggle("show");
}

function selectYear(year) {
    document.getElementById("selected-year").innerText = year;
}

// Close the dropdown menu if the user clicks outside of it
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
