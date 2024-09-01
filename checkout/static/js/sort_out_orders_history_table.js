function sortTable(column) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("ordersTable");
    switching = true;
    dir = "asc";
    
    while (switching) {
        switching = false;
        rows = table.rows;
        
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[column];
            y = rows[i + 1].getElementsByTagName("TD")[column];
            
            if (column === 1) { // Date column
                x = new Date(x.getAttribute("data-date"));
                y = new Date(y.getAttribute("data-date"));
            } else if (column === 2) { // Total column
                x = parseFloat(x.getAttribute("data-total"));
                y = parseFloat(y.getAttribute("data-total"));
            } else {
                x = x.innerHTML.toLowerCase();
                y = y.innerHTML.toLowerCase();
            }
            
            if (dir == "asc") {
                if (x > y) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x < y) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }

    // Call updateSortIcons after sorting
    updateSortIcons(column, dir);
}

function updateSortIcons(column, direction) {
    const icons = document.querySelectorAll('.sort-icon');
    icons.forEach(icon => {
        icon.classList.remove('fa-sort-up', 'fa-sort-down', 'sort-active');
        icon.classList.add('fa-sort');
    });

    const clickedIcon = document.querySelector(`.sort-icon[data-column="${column}"]`);
    if (clickedIcon) {
        clickedIcon.classList.remove('fa-sort');
        clickedIcon.classList.add('sort-active');

        if (direction === "asc") {
            clickedIcon.classList.add('fa-sort-up');
        } else {
            clickedIcon.classList.add('fa-sort-down');
        }
    }
}

// Add event listeners to sort icons when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const sortIcons = document.querySelectorAll('.sort-icon');
    sortIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const column = this.getAttribute('data-column');
            sortTable(parseInt(column));
        });
    });
});