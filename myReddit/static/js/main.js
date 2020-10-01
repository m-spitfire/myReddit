function navbarToggler() {
  document.addEventListener("DOMContentLoaded", () => {
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(
      document.querySelectorAll(".navbar-burger"),
      0
    );

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {
      // Add a click event on each of them
      $navbarBurgers.forEach((element) => {
        element.addEventListener("click", () => {
          // Get the target from the "data-target" attribute
          const target = element.dataset.target;
          const $target = document.getElementById(target);

          // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
          element.classList.toggle("is-active");
          $target.classList.toggle("is-active");
        });
      });
    }
  });
}

function messageDeleter() {
  document.addEventListener("DOMContentLoaded", () => {
    // Get all "message-header>delete" delete elements 
    (document.querySelectorAll(".message-header .delete") || []).forEach(
      ($delete) => {
        // Get the `parentNode` in order to delete
        $message_header = $delete.parentNode;
        $message = $message_header.parentNode;
        // add a click event for each of them
        $delete.addEventListener("click", () => {
          // remove the message
          $message.parentNode.removeChild($message);
        });
      }
    );
  });
}
function notificationDeleter() {
  document.addEventListener("DOMContentLoaded", () => {
     // Get all "notification>delete" delete elements 
    (document.querySelectorAll(".notification .delete") || []).forEach(
      ($delete) => {
        // Get the `parentNode` in order to delete
        $notification = $delete.parentNode;
        // add a click event for each of them
        $delete.addEventListener("click", () => {
          // remove the notification
          $notification.parentNode.removeChild($notification);
        });
      }
    );
  });
}
function mediaFunction() {
  // I do not want to have a column in the bottommost of the posts so remove when width is 760 px
  if (matchMedia("screen and (max-width: 760px)").matches) {
    var sidebar = document.getElementById("sidebar");
    sidebar.parentNode.removeChild(sidebar);
  }
}

function main() {
  navbarToggler();
  messageDeleter();
  notificationDeleter();
  mediaFunction();
}

main();
