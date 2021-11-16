let diary_data = [];
let filteredData = [];
let selected_index = null;

let post_domain = 'diaries_list_api';
let update_domain = 'diary_detail_api/';
const domain = post_domain;


// initialize tiny mce
tinymce.init({
    selector: '#mytextarea',
	plugins: 'a11ychecker advcode casechange export formatpainter linkchecker autolink lists checklist media mediaembed pageembed permanentpen powerpaste table advtable tinycomments tinymcespellchecker',
	toolbar: 'a11ycheck addcomment showcomments casechange checklist code export formatpainter pageembed permanentpen table',
	toolbar_mode: 'floating', 
	tinycomments_mode: 'embedded',
	tinycomments_author: 'Author name', 
});

// get the data from the server
const get_data = async () => {
	const res = await fetch(`${post_domain}?interval=${interval.value}`);
	const data = await res.json();
	// set the variable
	diary_data = data;
	return data;
}

const update_selected_index = (e) => {
	// the index of the selected element
	selected_index = e.srcElement.parentNode.id;
	displayContent(diary_data[selected_index]);

	// display detail
	displayDetail();
}

const displayList = () => {
	listDiv.style.display = "block";

	// hide detail
	detailDiv.style.display = "none";

	// hide create
	createUpdateDiv.style.display = "none";

	// hide delete
	deleteDiv.style.display = 'none';
}
			
const displayDetail = () => {
	detailDiv.style.display = "block";

	// hide list
	listDiv.style.display = "none";
}

const displayUpdateCreate = () => {
	createUpdateDiv.style.display = "block";

	// display post btn
	postBtn.style.display = 'block';

	// hide list
	listDiv.style.display = 'none';

	// hide update btn
	updateBtn.style.display = 'none';
}

const displayDelete = () => {
	deleteDiv.style.display = 'block';

	// display confirmation
	confirmationP.innerHTML += diary_data[selected_index].title + '?';

	// hide detail
	detailDiv.style.display = 'none';
}

// update
const displayUpdate = () => {
	displayUpdateCreate();
	const data = diary_data[selected_index];
	diaryTitle.value = data['title'];
	tinymce.get("mytextarea").setContent(data['content']);

	// display update 
	updateBtn.style.display = 'block';

	// hide post btn
	postBtn.style.display = 'none';

	// hide detail
	detailDiv.style.display = 'none';
}

const displayContent = (content) => {
	contentDiv.innerHTML = "";
	contentDiv.innerHTML = "<p>" + content["title"] + "<br>" + content["timestamp"] + "</p>";
	contentDiv.innerHTML += content["content"];
}

// update the table when the interval is changed
const updateTableOnIntervalChange = async () => {
	// get the data
	const data = await get_data();
	createTableWr();
}

// create a table base on fund and category
const createTableWr = () => {
	createT();
}

// initialize the list
const initialize = async () => {
	displayList();
	let data = await get_data();
	createTableWr();
}

// create
const get_diary_data = (type, domain) => {
	const url = domain;
	const csrftoken = getCookie('csrftoken');
	const diary_data = {
		title: diaryTitle.value,
		content: tinymce.get("mytextarea").getContent()
	};

	const request = new Request(url, {
		method: type,
		body: JSON.stringify(diary_data),
		headers: new Headers({
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		})
	});

	return request;
}

const post = async () => {
	const request = get_diary_data('POST', post_domain);
	const res = await fetch(request);
	const data = await res.json();

	// add the new data to the diary data
	diary_data.push(data);

	// update the table
	createTableWr();

	// hide the create
	createUpdateDiv.style.display = 'none';

	// display the list
	listDiv.style.display = "block";

	// clear the contents of the title and textbox
	diaryTitle.value = '';
	tinymce.get("mytextarea").setContent('');
}

const update = async () => {
	const request = get_diary_data('PUT', update_domain+diary_data[selected_index].id);
	const res = await fetch(request);
	const data = await res.json();

	// replace the updated content
	diary_data[selected_index] = data;

	// update the table
	createTableWr();

	// hide the create
	createUpdateDiv.style.display = 'none';

	// display the list
	listDiv.style.display = "block";	

	// clear the contents of the title and textbox
	diaryTitle.value = '';
	tinymce.get("mytextarea").setContent('');		
}

// delete
const del = async () => {
	const request = get_diary_data('DELETE', update_domain+diary_data[selected_index].id);
	await fetch(request);
	// delete the item
	delete diary_data[selected_index];

	// update the table
	createTableWr();

	// hide delete
	deleteDiv.style.display = 'none';

	// display list
	listDiv.style.display = 'block';
}

// diary list conponent
const listDiv = document.getElementById("list");
const tableDiv = document.getElementById("table-div");
const createDiaryBtn = document.getElementById("create-diary-btn");
const interval = document.getElementById("interval");



// detail
const detailDiv = document.getElementById("detail");
const contentDiv = document.getElementById("content-div");
const showTableBtn = document.getElementById("show-table-btn");

// create and update
const createUpdateDiv = document.getElementById('create-update');
let diaryTitle = document.getElementById('id_title');
const mytextarea = document.getElementById('mytextarea');
const postBtn = document.getElementById('post-btn');
const updateBtn = document.getElementById('update-btn');

// delete
const deleteDiv = document.getElementById('delete');
const confirmationP = document.getElementById('confirmation-p');


initialize();