function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

/* --- Searching a course --- */

/* --- Actions [Edit and Delete] --- */

function editCourse(courseID) {
  window.location.href = `/update_course/${courseID}`; // Redirect to the edit course page
}

function deleteCourse(courseID) {
  if (confirm("Are you sure you want to delete this course?")) {
    fetch("/dbapi/courses/" + courseID, {
      method: "DELETE",
    })
      .then((response) => {
        if (response.status === 204) {
          console.log("Course deleted successfully");
          const row = document.getElementById(`courseRow${courseID}`);
          if (row) {
            row.remove();
            alert("Course deleted successfully");
          } else {
            console.error("Could not find the row to delete in the DOM.");
            alert(
              "Course deleted from database, but the row was not found in the DOM."
            );
          }
        } else {
          // If the server responds but not with a 204 status, handle other responses
          return response.json().then((data) => {
            alert(
              "Error deleting course: " + (data.message || "Unknown error")
            );
          });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Network or processing error: " + error.message);
      });
  }
}

/*
function editPrerequisite(prerequisiteID) {
  // Logic to edit a prerequisite
  console.log("Editing prerequisite", prerequisiteID);
  // Redirect to the edit prerequisite page or open a modal for editing
}

function deletePrerequisite(prerequisiteID) {
  // Logic to delete a prerequisite
  console.log("Deleting prerequisite", prerequisiteID);
  // Make a request to the server to delete the prerequisite and then refresh the list
}*/

// Ensure the DOM is fully loaded before running the script
document.addEventListener("DOMContentLoaded", () => {
  // Open the Course Catalog tab by default
  openTab(new Event("click"), "CourseCatalog");
});
