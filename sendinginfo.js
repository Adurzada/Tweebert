

const button = document.getElementById('submitbutton');
const email = document.getElementById('email-2');
const mess = document.getElementById('message-2');
const res = document.getElementById('results-1')


const sendform = (em, mes) => {
  let formData = new FormData(document.getElementById("myform1"));
  formData.append("email",em);
  formData.append("query",mes);
  var val = '\n' + em + ' -> ' + mes;
  
  fetch("/", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(formData).toString(),
  })
    .then(() => res.innerHTML = ("Form successfully submitted for ") + em + ("\nWe will send you the report in less than a week!"))
    .catch((error) => alert(error));
};





button.onclick = function () {
  event.preventDefault();
  var em = email.value;
  var mes = mess.value;
  var val = em + '?:?:?' + mes;
  console.log(val)

  // Get the reciever endpoint from Python using fetch:

  fetch("http://127.0.0.1:5000/receiver",
    {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
        'Accept': 'application/json'
      },
      // Strigify the payload into JSON:
      body: JSON.stringify(val)
    }).then(res => {
      if (res.ok) {
        console.log(res)
        return res.json()
      } else {
        alert("something is wrong")
      }
    }).then(jsonResponse => {

      // Log the response data in the console
      console.log(jsonResponse)
      res.innerHTML = (jsonResponse)
    }
    ).catch((err) => sendform(em, mes));

}
