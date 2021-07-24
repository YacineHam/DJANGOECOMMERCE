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
    } else {
      updateCartItem(productId, action);
    }
  });
}
