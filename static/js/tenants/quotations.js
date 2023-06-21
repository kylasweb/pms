
    document.getElementById("company").addEventListener("change", function() {
        let companyId = this.value;
        let buildingSelect = document.getElementById("building");

        // Reset building options
        buildingSelect.innerHTML = '<option value="">Select a company first</option>';

        // Fetch buildings for the selected company
        const request_resource = '/admin/tenant/buildings/'+ companyId;
        if (companyId) {
            fetch(request_resource)
                .then(response => response.json())
                .then(data => {
                    // Populate building options
                    if (data.length > 0) {
                        buildingSelect.innerHTML = '';
                        data.forEach(function(building) {
                            let option = document.createElement('option');
                            option.value = building.id;
                            option.textContent = building.name;
                            buildingSelect.appendChild(option);
                        });
                    } else {
                        buildingSelect.innerHTML = '<option value="">No Vacant buildings found</option>';
                    }
                })
                .catch(error => {
                    console.log('Error:', error);
                });
        }
    });
