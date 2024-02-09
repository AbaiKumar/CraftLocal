var page = 0;
var addZoom = target => {
    let containers = document.getElementsByClassName(target);
    for (let i = 0; i < containers.length; i++) {
        let container = containers[i],
            imgsrc = container.currentStyle || window.getComputedStyle(container, false);
        imgsrc = imgsrc.backgroundImage.slice(4, -1).replace(/"/g, "");

        let img = new Image();
        img.src = imgsrc;
        img.onload = () => {
            container.onmousemove = e => {
                let rect = e.target.getBoundingClientRect(),
                    xPos = e.clientX - rect.left,
                    yPos = e.clientY - rect.top,
                    xPercent = xPos / (container.clientWidth / 100) + "%",
                    yPercent = yPos / ((container.clientWidth) / 100) + "%";

                Object.assign(container.style, {
                    backgroundPosition: xPercent + " " + yPercent,
                    backgroundSize: "300px"
                });
            };
            container.onmouseleave = e => {
                Object.assign(container.style, {
                    backgroundPosition: "center",
                    backgroundSize: "cover"
                });
            };
        }
    }
};

function dataLoader() {
    if(document.getElementById('products') == null) {
        return;
    }
    document.getElementById('products').innerHTML = "";
    fetch('/get_data?pageno=' + page)
        .then(response => response.json())
        .then(response => {
            response["data"].forEach(function (item) {
                var offer = item.Price - parseInt((item.Price * item.Discount) / 100);
                document.getElementById('products').innerHTML += `
                    <div class="card animate__animated animate__backInRight">
                        <a href="./singlePage?pid=`+ item._id + `" title="` + item.Name + `">
                            <div class="zoomC" style="background: url('uploads/`+ item.Name + `.jpg');oveflow : hidden;background-clip: padding-box;"></div>
                        </a>
                        <div class="details">
                            <h5>${item.Name}</h5>
                            <p>
                                ${(item.Discount === 0) ? `<em>₹${item.Price}</em>` : `<strike>₹${item.Price}</strike>&nbsp;&nbsp;<em><b>₹${offer}</b></em>`}
                            </p>
                            <button onclick="addToCart('`+ item._id + `','` + item.Name + `')">Add to Cart</button>
                        </div>
                    </div>
                `;
            });
        })
        .catch(error => console.error('Error:', error));
}

window.onload = function caller() {
    dataLoader(0);
    addZoom("zoomC");
    setInterval(dataLoader, 15000);
};

function addToCart(itemID, itemName) {
    fetch('/addItem?itemID=' + itemID)
        .then(response => response.json())  // Assuming the response is in JSON format
        .then(data => {
            console.log(data["result"]);
            if (data && data["result"] === true) {
                alert("Item '" + itemName + "' added to cart!!!");
            } else {
                alert("Item '" + itemName + "' failed!!!");
            }
        })
        .catch(error => console.error('Error:', error));
}