let diary_data = [];
let filteredData = [];
let selected_index = null;

let post_domain = 'diaries_list_api';
let update_domain = 'diary_detail_api';
const domain = post_domain;

const csrftoken = getCookie('csrftoken');


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
const get_data_wr = async () => {
	const domain = `${post_domain}?interval=${interval.value}`;
	const data = await get_data(domain)
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

	// display search bar
	searchBar.style.display = "block";
	
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

	// hide search bar
	searchBar.style.display = "none";
}

const displayUpdateCreate = () => {
	createUpdateDiv.style.display = "block";

	// display post btn
	postBtn.style.display = 'block';

	// hide list
	listDiv.style.display = 'none';

	// hide update btn
	updateBtn.style.display = 'none';

	// hide search bar
	searchBar.style.display = "none";
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

// search
const displaySearch = () => {
	searchDiv.style.display = 'block';

	// hide table
	listDiv.style.display = 'none';
}

const displayContent = (content) => {
	contentDiv.innerHTML = "";
	contentDiv.innerHTML = "<p>" + content["title"] + "<br>" + content["timestamp"] + "</p>";
	contentDiv.innerHTML += content["content"];
}

// update the table when the interval is changed
const updateTableOnIntervalChange = async () => {
	displayList();
	// get the data
	const data = await get_data_wr();
	createTableWr();
}

// create a table base on fund and category
const createTableWr = () => createTable(diary_data, ['title', 'timestamp'], tableDiv, update_selected_index);

const get_text_area_content = () => {
	const data = {
		title: diaryTitle.value,
		content: tinymce.get("mytextarea").getContent()
	};
	return data;
}

const post = async () => {
	const obj_data = get_text_area_content();
	const data = await post_update(post_domain, 'POST', obj_data, csrftoken);

	// post processing

	// add the new data to the diary data
	diary_data.push(data);

	// update the table
	createTableWr();

	// display the list
	displayList();

	// clear the contents of the title and textbox
	diaryTitle.value = '';
	tinymce.get("mytextarea").setContent('');
}

const update = async () => {
	const obj_data = get_text_area_content();
	const data = await post_update(`${update_domain}/${diary_data[selected_index].id}`, 'PUT', obj_data, csrftoken);


	// replace the updated content
	diary_data[selected_index] = data;

	// update the table
	createTableWr();

	// display the list
	displayList();

	// clear the contents of the title and textbox
	diaryTitle.value = '';
	tinymce.get("mytextarea").setContent('');		
}

// delete
const del_wr = async () => {
	const obj_data = get_text_area_content();
	const response = await del(`${update_domain}/${diary_data[selected_index].id}`, obj_data, csrftoken);

	// delete the item
	delete diary_data[selected_index];

	// update the table
	createTableWr();

	// display list
	displayList();
}

// search
function search(){
	const search_term = searchField.value;
	console.log(search_term);
	if(search_term.length != 0){
		// display search results
		displaySearch();
		searchDiv.innerHTML = '';
		searchDiv.innerHTML = search_term;
	}else{
		// hide search results
		searchDiv.style.display = 'none';

		// display list
		displayList();
	}
}

// diary list conponent
const listDiv = document.getElementById("list");
const tableDiv = document.getElementById("table-div");
const createDiaryBtn = document.getElementById("create-diary-btn");

const interval = document.getElementById("interval");
const newEntryBtn = document.getElementById("new-entry-btn");
const searchField = document.getElementById("search-field");

searchField.onchange = search;

// when the interval is changed update the table
interval.onchange = updateTableOnIntervalChange;

// when add new entry is clicked
newEntryBtn.onclick = displayUpdateCreate;



// detail
const detailDiv = document.getElementById("detail");
const contentDiv = document.getElementById("content-div");

const showTableBtn = document.getElementById("show-table-btn");
const displayUpdateBtn = document.getElementById("display-update-btn");
const displayDeleteBtn = document.getElementById("display-delete-btn");

showTableBtn.onclick = displayList;
displayUpdateBtn.onclick = displayUpdate;
displayDeleteBtn.onclick = displayDelete;


// create and update
const createUpdateDiv = document.getElementById('create-update');
let diaryTitle = document.getElementById('id_title');
const mytextarea = document.getElementById('mytextarea');

const postBtn = document.getElementById('post-btn');
const updateBtn = document.getElementById('update-btn');
const goBackBtn = document.getElementById("go-back-btn");

postBtn.onclick = post;
updateBtn.onclick = update;
goBackBtn.onclick = displayList;

// delete
const deleteDiv = document.getElementById('delete');
const confirmationP = document.getElementById('confirmation-p');

const deleteYesBtn = document.getElementById("delete-yes-btn");
const deleteNoBtn = document.getElementById("delete-no-btn");

deleteYesBtn.onclick = del_wr;
deleteNoBtn.onclick = displayList;


// search
const searchDiv = document.getElementById('search');

// search bar
const searchBar = document.getElementById('search-bar');

updateTableOnIntervalChange();