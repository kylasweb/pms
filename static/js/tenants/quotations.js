document.addEventListener("DOMContentLoaded", function() {
    const company_selector = document.getElementById("company");
    const booking_type_selector = document.getElementById('booking_type');
    company_selector.addEventListener("change", function () {
        let companyId = company_selector.value;
        console.log(company_selector);
        let buildingSelect = document.getElementById("building");

        // Reset building options
        buildingSelect.innerHTML = '<option value="">Select a company first</option>';

        // Fetch buildings for the selected company
        const request_resource = '/admin/tenant/buildings/' + companyId;
        console.log(companyId)
        if (companyId) {
            console.log('making request to ' + companyId);
            fetch(request_resource)
                .then(response => response.json())
                .then(data => {
                    // Populate building options
                    if (data.length > 0) {
                        buildingSelect.innerHTML = '';
                        data.forEach(function (building) {
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
    })

    booking_type_selector.addEventListener("change", function(){

    })

})
