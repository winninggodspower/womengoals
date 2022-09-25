let errors = []

$('#volunteer-form').on('submit', (e)=>{
    e.preventDefault()

    let selectFields = $('#volunteer-form').find("select");
    for (let i = 0; i < selectFields.length; i++) {
        const field = selectFields[i];

        if (field.value === `Choose ${field.id}`){
            errors.push({
                field: field.id,
                message: 'Please select an option'
            })
            field.classList += ' is-invalid'

        }else{
            if ($(field).hasClass("is-invalid")){
                $(field).removeClass("is-invalid")
            }
        }
        
    }


    if (errors.length <= 0){

        $('#volunteer-form').unbind().submit();

    }else{

        errors.forEach((error)=>{
            $(`#${error.field}-error-field`).text(error.message)
        })
        errors = []
    }


    
    
})


function convertFormToJSON(form) {
   json = {
    username: form.find("[name=username]").val(),
    phone: form.find("[name=phone]").val(),
    country: form.find("[name=country]").val(),
    state: form.find("[name=state]").val(),
    department: form.find("[name=department]").val(),
   }
   console.log(json);
    return json;
  }