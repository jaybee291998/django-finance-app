const months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

// get the data from the server
async function get_data(domain){
	const res = await fetch(domain);
	const data = await res.json();
	return data;
}

// create a table base on fund and category
function createTable(raw_data, data_properties, tableDiv, row_selection_func){
	// table to tabulate all of the expense data
	let table = document.createElement("TABLE");
	table.className = "table table-striped";
	// loop thriugh all the expense data
	// and create a row for each expense entry
	raw_data.forEach((data, i) => {
		// insert a row on table for each expense entry
		let row = table.insertRow(i);
		row.id = i;
		row.onclick = row_selection_func;
		// the properties of the expense such as desctription, price, ...etc
		data_properties.forEach((data_property, j) => {
			// the value of the expense property i.e. description="pambili ng ulam"
			let data_property_value = data[data_property];
			// add the cells that contain the properties of the expenses
			let cell = row.insertCell(j);
			cell.textContent = data_property_value;
		});
	});
	// empty the div first before adding the new table
	tableDiv.innerHTML = '';
	tableDiv.appendChild(table);
}


function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
		    var cookie = cookies[i].trim();
		    if (cookie.substring(0, name.length + 1) === (name + '=')) {
		    	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		    	break;
		    }
		}
	}
	return cookieValue;
}

// get the request object
function get_request_obj(type, domain, data, csrftoken){
	const url = domain;
	const request = new Request(url, {
		method: type,
		body: JSON.stringify(data),
		headers: new Headers({
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		})
	});

	return request;
}

// post and put
async function post_update(domain, type, obj_data, csrftoken){
	const request = get_request_obj(type, domain, obj_data, csrftoken);
	const res = await fetch(request);
	const data = await res.json();
	return data;
}


// delete
async function del(domain, data, csrftoken){
	const request = get_request_obj('DELETE', domain, data, csrftoken);
	const response = await fetch(request);
	return response;
}


// convert raw timestamp into a more huma readbable format
function convert_date(raw_date){
	const year_str = raw_date.substr(0, 4);
	const month_str = raw_date.substr(5, 2);
	const day_str = raw_date.substr(8, 2);

	return `${months[parseInt(month_str)]} ${day_str}, ${year_str}`
}

function convert_time(raw_time){
	let hour = parseInt(raw_time.substr(0, 2));
	let timestamp = 'AM';
	if(hour > 12){
		timestamp = 'PM';
		hour -= 12;
	}

	return `${hour}${raw_time.slice(2)} ${timestamp}`;
}

function processDateStr(date_str){
	const date = convert_date(date_str.slice(0, 10));
	const time = convert_time(date_str.slice(11, 19));

	return `${date} ${time}`;
}