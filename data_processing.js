var expenses = [100, 100, 12, 10, 10, 67, 100, 12, 60, 56, 56];
var dates = [17, 18, 18, 19, 19, 19, 20, 20, 20, 21, 22];


const count_occurence = (array) =>{
	occurence_count = {}
	for(let i = 0; i < array.length; i++){
		let val = array[i];
		if(occurence_count.hasOwnProperty(val)){occurence_count[val]["count"]++;}
		else{ occurence_count[val] = { start_index:i,count:1};}
	}
	return occurence_count
}

const som = (array, occurence_count) => {
	var new_array = []
	for(let key in occurence_count){
		start_index = occurence_count[key].start_index;
		end_index = start_index + occurence_count[key].count;

		var sum = sum_fr_to(array, start_index, end_index);
		new_array.push(sum)
	}
	return new_array;
}

const get_chart_data = (array_1, array_2) => {
	var chart_data = {data:[], labels:[]}
	var i = 0;
	while(i < array_2.length){
		let cur_val = array_2[i];
		let count = count_consec_occur(array_2, i, cur_val);
		let sum = sum_fr_to(array_1, i, i+count);
		chart_data["data"].push(sum);
		chart_data["labels"].push(cur_val)
		i += count;
	} 
	return chart_data;
}

const count_consec_occur = (array, start_index, element) => {
	var occurence_count = 0;
	for(let i = start_index; i < array.length; i++){
		var cur_val = array[i];
		if(cur_val == element){ occurence_count++ }
		else{ break; }
	}
	return occurence_count;
}

const sum_fr_to = (array, start_index, end_index) => {
	sum = 0;
	for(let i = start_index; i < end_index; i++){
		sum += array[i];
	}
	return sum
}

// var occurence_count = count_occurence(dates);
// var new_array = som(expenses, occurence_count);
// console.log(new_array);

var a = get_chart_data(expenses, dates)
// var new_array = [];
// var j = 0;
// for(let i = 0; i < dates.length; i++){
// 	let cur_val = dates[j];
// 	let count = count_consec_occur(dates, j, cur_val);
// 	let sum = sum_fr_to(expenses, j, j+count);
// 	new_array.push(sum);
// 	j += count;
// }
console.log(a);