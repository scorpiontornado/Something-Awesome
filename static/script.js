const sqli1_user_in = document.getElementById("sqli1_form_username");
const sqli1_user_out = document.getElementById("sqli1_query_username");
sqli1_user_in.addEventListener("input", (e) => {
  sqli1_user_out.textContent = sqli1_user_in.textContent;
});

const sqli1_pass_in = document.getElementById("sqli1_form_password");
const sqli1_pass_out = document.getElementById("sqli1_query_password");
sqli1_pass_in.addEventListener("input", (e) => {
  sqli1_pass_out.textContent = sqli1_pass_in.textContent;
});