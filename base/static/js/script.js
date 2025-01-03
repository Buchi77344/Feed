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
			event.target.closest(highlightEl) == null // event.target.closest(`[data-select = "${dropEl.dataset.select}"]`) == null
		) {
			removePopup(dropEl);
		}

		// console.log(highlightEl);
		console.log(dropEl.dataset.select);
	});
}

/** Profile Page script */

if (document.querySelector(".profile.page")) {
	let profileUtilItemHead = document.querySelectorAll(
		".profile-util-item-head"
	);
	let allProfileinfo = document.querySelectorAll(
		".profile-info-wrapper .info-item"
	);

	profileUtilItemHead[0].classList.add("active");

	profileUtilItemHead.forEach((el, index) => {
		el.addEventListener("click", function () {
			removeOtherOption(index);
			profileUtilItemHead[index].classList.toggle("active");
			let ctaSet = this.dataset.profile_cta;

			allProfileinfo.forEach((info) => {
				info.classList.add("hide");
				info.classList.remove("reveal");
				if (ctaSet == info.dataset.profile_category) {
					info.classList.remove("hide");
					info.classList.add("reveal");
				}
			});

			let parent = this.parentElement;
			console.log(parent);
			let mobileProfileInfo = parent.querySelector(
				".profile-donations-container.mobile"
			);
			mobileProfileInfo.classList.toggle("slide-down");
		});
	});

	function removeOtherOption(index) {
		profileUtilItemHead.forEach((el, i) => {
			if (i !== index) {
				el.classList.remove("active");
			}
		});
	}
}

/** Profile Page script */

const existingRadioEl = document.querySelectorAll(
	"input[name = 'existing_radio']"
);
const existingCta = document.querySelectorAll(".existing-cta-div");
let selectedRadio = null;

const supportCtaBtn = document.querySelectorAll(".support-cta-container .btn");
const supportCtaTabs = document.querySelectorAll(".support-tab");

existingRadioEl.forEach((radio) => {
	radio.addEventListener("click", function () {
		if (selectedRadio == this) {
			this.checked = false;
			selectedRadio = null;
		} else {
			selectedRadio = this;
		}

		existingCta.forEach((cta) => {
			if (radio.id == cta.dataset.content) {
				cta.classList.add("show");
			} else {
				cta.classList.remove("show");
			}
		});
	});
});

supportCtaBtn.forEach((btn) => {
	btn.addEventListener("click", function () {
		btn.classList.remove("active");
		supportCtaTabs.forEach((tab) => {
			if (btn.id == tab.dataset.content) {
				tab.classList.add("show");
			} else {
				tab.classList.remove("show");
			}
		});
	});
});
