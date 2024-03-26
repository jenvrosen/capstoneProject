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

/* --- Creating a course --- */
function createCourse() {
  const title = document.getElementById("title").value;
  const department = document.getElementById("department").value;
  const description = document.getElementById("description").value;

  fetch("/dbapi/courses", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: title,
      description: description,
      department: department,
    }),
  })
    .then((response) => {
      if (response.ok) {
        alert("Course created successfully");
        window.location.href = "/admin";
      } else {
        return response.json().then((data) => {
          throw new Error(
            data.message || "An error occurred while creating the course"
          );
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error creating course: " + error.message);
    });
}

/* --- Actions [Edit and Delete] --- */

//To navigate to edit course page
function editCourse(courseID) {
  window.location.href = `/edit_course/${courseID}`; // Redirect to the edit course page
}

function updateCourse(courseID) {
  const title = document.getElementById("title").value;
  const department = document.getElementById("department").value;
  const description = document.getElementById("description").value.trim();

  fetch(`/dbapi/courses/${courseID}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: title,
      description: description,
      department: department,
    }),
  })
    .then((response) => {
      if (response.ok) {
        alert("Course updated successfully");
        window.location.href = "/admin";
      } else {
        response.json().then((data) => {
          alert("Failed to update course: " + data.message);
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while updating the course");
    });
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
