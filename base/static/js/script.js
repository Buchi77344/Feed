let dropDownHead = document.querySelectorAll(".select-head");
let selectDropDown = document.querySelectorAll(".select-dropdown");
if (document.querySelector(".select-head")) {
	dropDownHead.forEach((dropHead) => {
		dropHead.addEventListener("click", function () {
			let parent = dropHead.parentElement;
			let selectDropDown = parent.querySelector(".select-dropdown");
			if (selectDropDown.classList.contains("popup")) {
				removePopup(selectDropDown);
			} else {
				addPopup(selectDropDown);
			}
			allRemovePopup(
				`[data-select = "${parent.dataset.select}"]`,
				selectDropDown
			);
		});
	});
}

function removePopup(dropElement) {
	dropElement.classList.add("popup-remove");
	dropElement.classList.remove("popup");
	setTimeout(() => {
		dropElement.style.display = "none";
	}, 500);
}

function addPopup(dropElement) {
	dropElement.style.display = "block";
	dropElement.classList.add("popup");
	dropElement.classList.remove("popup-remove");
}

function allRemovePopup(highlightEl, dropEl) {
	document.addEventListener("click", function (event) {
		if (
			event.target.closest(highlightEl) == null		// event.target.closest(`[data-select = "${dropEl.dataset.select}"]`) == null
		) {
			removePopup(dropEl);
		}

        // console.log(highlightEl);
				console.log(dropEl.dataset.select);
	});
}

let profileUtilItemHead = document.querySelectorAll(".profile-util-item-head")
profileUtilItemHead.forEach((el, index) => {
	el.addEventListener("click", function(){
		removeOtherOption(index)
		profileUtilItemHead[index].classList.toggle("active");

	})
})

function removeOtherOption(index) {
	profileUtilItemHead.forEach((el, i) => {
		if (i !== index) {
			el.classList.remove("active");
		}
	});
}
