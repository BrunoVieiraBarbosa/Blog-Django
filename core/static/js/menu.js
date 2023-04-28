const searhInput = document.getElementById('search');
const optionsList = document.getElementById('options-list');
var text_search = "";
var response = {};

addEventListener('input', (event) => {
    text_search = searhInput.value;
    if (text_search.length >= 3){
        fetch(
            'http://127.0.0.1:8000/api/search/'+text_search, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        ).then(
            (resp) => resp.json()
        ).then(
            (data) => {addOptionsInput(data)}
        )
    } else {
        optionsList.innerHTML = "";
    }
})

function addOptionsInput(response) {
    optionsList.innerHTML = "";

    for (var i in response){
        var listItem = response[i];
        for (var text=0; text < listItem.length; text++){
            optionsList.innerHTML += "<option>" + listItem[text] + "</option>";
        }
    }
}
