/* admin.js */
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
function searchCourses() {
  const searchInput = document.getElementById("search").value.trim();
  if (searchInput) {
    window.location.href = `/search_results?search=${encodeURIComponent(
      searchInput
    )}`;
  } else {
    alert("Please enter a course name to search.");
  }
}

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

/* --- Assign Prerequisite --- */
function assignPrerequisite() {
  const courseID = document.getElementById("courseID").value;
  const prerequisiteCourseID = document.getElementById(
    "prerequisiteCourseID"
  ).value;

  fetch("/dbapi/course-prerequisites", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      courseID: courseID,
      prerequisiteCourseID: prerequisiteCourseID,
    }),
  })
    .then((response) => {
      if (response.ok) {
        alert("Prerequisite created successfully");
        window.location.href = "/admin"; // or navigate as needed
      } else {
        return response.json().then((data) => {
          throw new Error(
            data.message || "An error occurred while creating the prerequisite"
          );
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error creating prerequisite: " + error.message);
    });
}

/* --- Select Entries [Bulk Delete] --- */
document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll(".delete-checkbox");
  const deleteSelectedButton = document.getElementById("delete-selected");

  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
      const anyChecked = Array.from(checkboxes).some((c) => c.checked);
      deleteSelectedButton.style.display = anyChecked ? "block" : "none";
    });
  });

  window.deleteSelectedCourses = function () {
    const selectedCourses = Array.from(
      document.querySelectorAll(".delete-checkbox")
    )
      .filter((c) => c.checked)
      .map((c) => c.getAttribute("data-course-id"));

    if (confirm("Are you sure you want to delete these courses?")) {
      selectedCourses.forEach((courseID) => {
        fetch(`/dbapi/courses/${courseID}`, {
          method: "DELETE",
        })
          .then((response) => {
            if (response.ok) {
              console.log("Course deleted successfully:", courseID);
              const row = document.getElementById(`courseRow${courseID}`);
              if (row) {
                row.remove(); // Ensures the DOM is updated
              }
            } else {
              console.error("Failed to delete the course", courseID);
              alert("Failed to delete the course: " + courseID);
            }
          })
          .catch((error) => {
            console.error("Error deleting course:", courseID, error);
            alert("Error deleting course: " + courseID + " - " + error);
          });
      });
      // Hide the delete button after processing all deletions
      document.getElementById("delete-selected").style.display = "none";
    }
  };
});

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

// Ensure the DOM is fully loaded before running the script
document.addEventListener("DOMContentLoaded", () => {
  // Open the Course Catalog tab by default
  openTab(new Event("click"), "CourseCatalog");
});
