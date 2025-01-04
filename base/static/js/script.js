let dropDownHead = document.querySelectorAll(".select-head");
let selectDropDown = document.querySelectorAll(".select-dropdown");
if (document.querySelector(".select-head")) {
	dropDownHead.forEach((dropHead) => {
		dropHead.addEventListener("click", function () {
			let parent = dropHead.parentElement;
			let selectDropDown = parent.querySelector(".select-dropdown");
			console.log(parent);
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

if (document.querySelector(".existing-cta-div")) {
	const existingRadioEl = document.querySelectorAll(
		"input[name = 'existing_radio']"
	);
	const existingCta = document.querySelectorAll(".existing-cta-div");
	let selectedRadio = null;

	const supportCtaBtn = document.querySelectorAll(
		".support-cta-container .btn"
	);
	const supportCtaTabs = document.querySelectorAll(".support-tab");

	const feedPayoutCategoryCta = document.querySelectorAll(
		".feed-payout-category-cta"
	);
	const feedPayoutCategory = document.querySelectorAll(".feed-payout-category");

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
			let btnDataset = btn.dataset.content;
			tabChangeFunc(supportCtaBtn, supportCtaTabs, this, btnDataset);
		});
	});

	feedPayoutCategoryCta.forEach((cta) => {
		cta.addEventListener("click", function () {
			let ctaDataset = cta.dataset.content;
			tabChangeFunc(
				feedPayoutCategoryCta,
				feedPayoutCategory,
				this,
				ctaDataset
			);
		});
	});

	function tabChangeFunc(allbtns, allTabs, el, btnDataset) {
		allbtns.forEach((btn) => btn.classList.remove("active"));
		el.classList.add("active");
		allTabs.forEach((tab) => {
			tab.classList.remove("show");
			document.querySelector(`#${btnDataset}`).classList.add("show");
		});
	}
}

//Dropdown

if (document.querySelector(".dropdown-util")) {
	let dropdownBtn = document.querySelectorAll(".dropdown-util-btn");
	let dropdown = document.querySelectorAll(".dropdown-util");
	let dropdownItem = document.querySelectorAll(".dropdown-util-item");
	let currencySpan = document.querySelectorAll(".curr-span");

	dropdownBtn.forEach((btn, index) => {
		btn.addEventListener("click", function () {
			console.log("work");
			dropdown[index].classList.toggle("show");
		});
	});

	dropdownItem.forEach((item) => {
		item.addEventListener("click", () => {
			let dropdownBtn =
				item.parentElement.parentElement.querySelector(".dropdown-util-btn");
			dropdownBtn.textContent = item.textContent;
			changeCurrency(item.textContent);
		});
	});

	function changeCurrency(currency) {
		let currVal = "";
		if (currency == "ZAR") {
			currVal = "R" + " ";
		} else if (currency == "USD") {
			currVal = "$";
		}

		currencySpan.forEach((curr) => {
			curr.textContent = currVal;
		});
	}

	document.addEventListener("click", (event) => {
		if (!event.target.matches(".dropdown-util-btn")) {
			dropdown.forEach((dp) => {
				if (dp.classList.contains("show")) {
					dp.classList.remove("show");
				}
			});
		}
	});
}

if (document.querySelector(".recurring-btn")) {
	let recurringBtn = document.querySelector(".recurring-btn");
	let oneOffBtn = document.querySelector(".one-off-btn");
	let recurringSelectContainer = document.querySelector(
		".recurring-select-container"
	);
	recurringBtn.addEventListener("click", function () {
		recurringSelectContainer.classList.add("show");
		if (oneOffBtn.classList.contains("active")) {
			oneOffBtn.classList.remove("active");
		}
		this.classList.add("active");
	});

	oneOffBtn.addEventListener("click", function () {
		recurringSelectContainer.classList.remove("show");
		if (recurringBtn.classList.contains("active")) {
			recurringBtn.classList.remove("active");
		}
		this.classList.add("active");
	});

	let donationPrice = document.querySelectorAll(".make-donation-cta-primary");
	let donationAmountInput = document.querySelector(".donation-amount-input");

	donationPrice.forEach((cta) => {
		cta.addEventListener("click", function () {
			donationPrice.forEach(cta => cta.classList.remove("active"))
			this.classList.add("active");
			let num = this.querySelector(".text").textContent;
			console.log((num.slice(0, num.length - 3)).trim());
			donationAmountInput.value = (num.slice(0, num.length - 3)).trim();
		});
	});
}
