$(document).ready(()=>{
    const API_KEY = 'clJ1bkpEYkRVemZTa21kSTNMd1dCOXJudDB1eW9wQ0Y1OEZhdGppMw==';
    let countryList ;

    const countryForm = $('#country-form');
    const stateForm = $('#state-form');

    countryForm.on('change',(option)=>{
      stateForm.attr('disabled', false)
      selectedOption = option.currentTarget.value;
      console.log(countryList);
      selectedOptionOsi = countryList.filter((country)=> country.name == selectedOption)[0]
      console.log(selectedOptionOsi);
      getStates(selectedOptionOsi.iso2)
    })

    $.ajax({
        url: 'https://api.countrystatecity.in/v1/countries',
        method: 'GET',
        headers: {
            'X-CSCAPI-KEY': API_KEY
          },
        success: function(data){
            countryList = data
            createCountryOptions(countryList)

        }
    });

    const createCountryOptions = (data)=>{
      data.forEach(country => {
        const countryOption = new Option();
        countryOption.value = country.name
        countryOption.innerText = country.name
        countryForm.append(countryOption)
      });
    }

    const getStates = async (countryIso2) => {
      console.log(countryIso2);
      await $.ajax({
        url: `https://api.countrystatecity.in/v1/countries/${countryIso2}/states`,
        method: 'GET',
        headers: {
            'X-CSCAPI-KEY': API_KEY
          },
        success: function(data){
            let stateList = data.map((data)=> data.name )
            console.log(stateList);
            createStateOption(stateList)
        }
      
      });
     }
  

    const createStateOption = (stateList)=>{
      stateForm.empty()
      stateForm.append('<option selected>Choose state</option>');
      stateList.forEach(state=>{
        const stateOption = new Option();
        stateOption.value = state
        stateOption.innerText = state
        stateForm.append(stateOption)

      })
    }

})