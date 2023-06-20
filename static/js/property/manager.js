    const container = document.getElementById("add-unit-container");
    const button = document.getElementById("add-unit-btn");

    button.addEventListener("click", function() {
        if (container.style.display === "none") {
            container.style.display = "block";
            button.innerHTML = "<i class='ti-close'> </i> Close Editor";
            button.className = "btn btn-danger"
        } else {
            container.style.display = "none";
            button.innerHTML = "<i class='ti-folder'></i> Open Unit Editor";
            button.className = "btn btn-primary";
        }
    });