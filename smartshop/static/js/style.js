


function showAddress(method){

document.getElementById("addressSection").style.display = "block";

if(method === "cod"){
document.getElementById("codButton").style.display = "block";
document.getElementById("upiButton").style.display = "none";
document.getElementById("paymentMethod").value = "Cash on Delivery";
}

if(method === "upi"){
document.getElementById("codButton").style.display = "none";
document.getElementById("upiButton").style.display = "block";
document.getElementById("paymentMethod").value = "Online Payment (Razorpay)";
}

}


/* Razorpay Payment */

if (typeof Razorpay !== "undefined") {

var options = {
key: razorpay_key,
amount: razorpay_amount,
currency: "INR",
name: "SmartShop",
description: "Order Payment",
order_id: razorpay_order_id,

handler: function (response) {

document.getElementById("paymentMethod").value = "Online Payment (Razorpay)";

/* submit form after payment success */
document.querySelector("form").submit();

}

};

var rzp = new Razorpay(options);

document.getElementById("upiButton").onclick = function(e){
rzp.open();
e.preventDefault();
};

}