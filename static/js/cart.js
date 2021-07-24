var updateButtons = document.getElementsByClassName("update-btn");
function updateCartItem(productId, action) {
  let data = { id: productId, action: action };
  fetch("/update_cart/", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "X-CSRFToken": csrftoken,
    },
  })
    .then((res) => {
      console.log("request complete !", res);
    })
    .then((data) => {
      console.log("data", data);
      location.reload();
    });
}

for (let index = 0; index < updateButtons.length; index++) {
  updateButtons[index].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log(productId, action);
    console.log("USER", user);
    if (user === "AnonymousUser") {
      addCookieItem(productId, action);
      location.reload();
    } else {
      updateCartItem(productId, action);
    }
  });
}

function addCookieItem(productId, action1) {
  if (action1 == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
      console.log("created");
    } else {
      cart[productId]["quantity"] += 1;
      console.log("added");
    }
  }
  if (action1 == "remove") {
    cart[productId]["quantity"] -= 1;
    console.log("deleted");
    if (cart[productId]["quantity"] <= 0) delete cart[productId];
  }
  console.log(cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
}
