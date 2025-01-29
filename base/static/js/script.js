let dropDownHead = document.querySelectorAll(".select-head");
let selectDropDown = document.querySelectorAll(".select-dropdown");
console.log(document.querySelector(".profile-util-item-head"));
console.log(document.querySelector(".nav-util-cta-container .search-icon-btn"));

if (document.querySelector(".select-head")) {
	dropDownHead.forEach((dropHead) => {
		dropHead.addEventListener("click", function () {
			let parent = dropHead.parentElement;
			let selectDropDown = parent.querySelector(".select-dropdown");
			console.log(parent);
			if (selectDropDown.classList.contains("scaleup")) {
				removePopup(selectDropDown);
			} else {
				addPopup(selectDropDown);
			}
			allRemovePopup(
				`[data-select = "${parent.dataset.select}"]`,
				selectDropDown
			);
			const selectAllInput = parent.querySelector(".select-all-input");
			selectAllInput.addEventListener("change", function () {
				const allInputs = parent.querySelectorAll(".terms-label input");
				allInputs.forEach((input) => {
					input.checked = this.checked;
				});
			});
		});
	});
}

function removePopup(dropElement) {
	dropElement.classList.add("scaleup-remove");
	dropElement.classList.remove("scaleup");
	setTimeout(() => {
		dropElement.style.display = "none";
	}, 500);
}

function addPopup(dropElement) {
	dropElement.style.display = "block";
	dropElement.classList.add("scaleup");
	dropElement.classList.remove("scaleup-remove");
}

function allRemovePopup(highlightEl, dropEl) {
	document.addEventListener("click", function (event) {
		if (
			event.target.closest(highlightEl) == null // event.target.closest(`[data-select = "${dropEl.dataset.select}"]`) == null
		) {
			removePopup(dropEl);
		}
	});
}

/** Profile Page script */
if (document.querySelector("main.profile")) {
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
			let mobileProfileInfo = parent.querySelector(".down-profile-cta.mobile");
			let dropdownHeight = mobileProfileInfo.scrollHeight;
			parent.style.setProperty("--dropdown-height", `${dropdownHeight + 20}px`);
			mobileProfileInfo.classList.toggle("slide-down");

			showViewMoreBtn();
		});
	});

	function removeOtherOption(index) {
		profileUtilItemHead.forEach((el, i) => {
			if (i !== index) {
				el.classList.remove("active");
			}
		});
	}

	function showViewMoreBtn() {
		// const viewMoreBtn = document.querySelectorAll(
		//   ".my-campaigns.view-more-btn"
		// );
		const profileCampaignsContainer = document.querySelectorAll(
			".profile-info-wrapper .profile-campaigns-container:not(.down-profile-cta)"
		);
		const mobileProfileCampaignsContainer = document.querySelectorAll(
			".profile-campaigns-container.down-profile-cta"
		);

		if (profileCampaignsContainer[0].classList.contains("reveal")) {
			// console.log(profileCampaignsContainer[0])
			let viewMoreBtn =
				profileCampaignsContainer[0].parentElement.querySelector(
					".my-campaigns.view-more-btn"
				);
			viewMoreBtn.classList.remove("hidden");
		} else {
			let viewMoreBtn =
				profileCampaignsContainer[0].parentElement.querySelector(
					".my-campaigns.view-more-btn"
				);
			viewMoreBtn.classList.add("hidden");
		}

		console.log(mobileProfileCampaignsContainer);

		if (mobileProfileCampaignsContainer[0].classList.contains("slide-down")) {
			let viewMoreBtn =
				mobileProfileCampaignsContainer[0].parentElement.querySelector(
					".my-campaigns.view-more-btn"
				);
			viewMoreBtn.classList.remove("hidden");
		} else {
			let viewMoreBtn =
				mobileProfileCampaignsContainer[0].parentElement.querySelector(
					".my-campaigns.view-more-btn"
				);
			viewMoreBtn.classList.add("hidden");
		}
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

	const donationPrice = document.querySelectorAll(".make-donation-cta-primary");
	const donationAmountInput = document.querySelector(".donation-amount-input");
	const donationPriceText = document.querySelectorAll(".donation-price-text");

	donationPrice.forEach((cta) => {
		cta.addEventListener("click", function () {
			donationPrice.forEach((cta) => cta.classList.remove("active"));
			this.classList.add("active");
			let num = this.querySelector(".text").textContent;
			let trimNum = num.slice(0, num.length - 3).replace(/\s/g, "");
			// console.log(trimNum);

			donationAmountInput.value = trimNum;
			console.log(num);
			donationPriceText.forEach((text) => (text.textContent = num));
			calcDonateSliderVal();
			const paymentLink = document.getElementById("payment-link");
			paymentLink.style.pointerEvents = "auto"; // Enable the link
			paymentLink.style.opacity = "1"; // Make the link visually active
		});
	});

	const sliderContainer = document.querySelector(".slider-container");
	const sliderBar = document.querySelector(".slider-bar");
	const sliderHandle = document.querySelector(".slider-handle");
	const sliderMarks = document.querySelector(".slider-marks");
	const donationBarCalcWrapper = document.querySelector(
		".donate-bar-calculation-container"
	);
	const donationBarPercent = document.querySelector(".donate-bar-percent");
	const donationBarCalcVal = document.querySelector(".donate-bar-calc-val");

	let currentPercentage = 0;
	let isDragging = false;
	const maxPercentage = 30; // Total range is 30%
	const numberOfMarks = 15; // 15 marks representing increments
	const initialIncrement = 1; // Initial increment for first mark
	const subsequentIncrement = 2; // Subsequent increment for odd numbers

	// Create marks
	for (let i = 0; i < numberOfMarks; i++) {
		const mark = document.createElement("div");
		mark.classList.add("slider-mark");
		mark.addEventListener("click", () => handleMarkClick(i));
		sliderMarks.appendChild(mark);
	}

	sliderHandle.addEventListener("mousedown", startDrag);
	window.addEventListener("mouseup", endDrag);
	window.addEventListener("mousemove", drag);

	sliderHandle.addEventListener("touchstart", startDrag);
	window.addEventListener("touchend", endDrag);
	window.addEventListener("touchmove", drag);

	sliderContainer.addEventListener("click", (e) => {
		if (!isDragging) updatePosition(e);
	});

	function startDrag(e) {
		isDragging = true;
		updatePosition(e);
	}

	function endDrag() {
		isDragging = false;
	}

	function drag(e) {
		if (!isDragging) return;
		updatePosition(e);
	}

	function updatePosition(e) {
		const rect = sliderContainer.getBoundingClientRect();
		const position = getPositionX(e);
		let offset = position - rect.left;
		offset = Math.max(0, Math.min(offset, rect.width)); // Ensure within bounds

		const percentage = (offset / rect.width) * maxPercentage;
		currentPercentage = calculateOddPercentage(percentage);
		donationBarPercent.textContent = Math.floor(currentPercentage) + "%";
		updateSlider(currentPercentage);
	}

	function getPositionX(e) {
		console.log(e);
		return e.type.includes("mouse") ? e.pageX : e.touches[0].clientX;
	}

	function updateSlider(percentage) {
		const displayedPercentage = (percentage / maxPercentage) * 100;
		sliderBar.style.width = `${displayedPercentage}%`;
		sliderHandle.style.left = `${displayedPercentage}%`;
		donationBarCalcWrapper.style.left = `${displayedPercentage}%`;
		calcDonateSliderVal(displayedPercentage);
	}

	function handleMarkClick(markIndex) {
		let targetPercentage = initialIncrement + markIndex * subsequentIncrement;
		currentPercentage = Math.min(targetPercentage, maxPercentage); // Cap at maxPercentage
		donationBarPercent.textContent = Math.floor(currentPercentage) + "%";
		updateSlider(currentPercentage);
	}

	function calculateOddPercentage(percentage) {
		// Convert percentage to the nearest odd percentage
		const oddPercentage =
			Math.ceil(percentage / subsequentIncrement) * subsequentIncrement;
		return Math.min(oddPercentage, maxPercentage); // Ensure it doesn't exceed maxPercentage
	}

	function calcDonateSliderVal() {
		let percent = donationBarPercent.textContent;
		let inputVal;
		if (donationAmountInput.value == "") {
			inputVal = 0;
		} else {
			inputVal = Number(donationAmountInput.value);
		}
		let val = (Number(percent.split("%")[0]) / 100) * inputVal;
		donationBarCalcVal.textContent = val.toFixed(2);
	}

	const donationSwitch = document.querySelector(".donation.switch");
	const donationSwitchInput = document.querySelector(
		".donation.switch .switch-input"
	);
	const donationNameInput = document.querySelector(".donation-name-input");

	donationSwitch.addEventListener("click", function () {
		if (donationSwitchInput.checked) {
			donationNameInput.classList.add("hide");
		} else {
			donationNameInput.classList.remove("hide");
		}
	});
}

//Percentage Progress

if (document.querySelector(".percent-progress")) {
	let percentProgress = document.querySelectorAll(".percent-progress");
	percentProgress.forEach(function (pr) {
		let progressBar = pr.querySelector(".percent-progress-bar");
		setTimeout(() => {
			progressBar.style.width = `${pr.dataset.percent}%`;
		}, 1000);
	});
}

//Client Side Validation
const submitBtn = document.querySelector(".cta-btn.submit-btn");
const acctForm = document.querySelector("[data-attr = 'acct-form-el']");

// const inputs = acctForm.querySelectorAll(".acct-input");

// Attach event listeners to each input for clearing error messages on focus
// inputs.forEach((input) => {
// 	input.addEventListener("focus", clearErrorMessage);
// 	input.addEventListener("input", () => validateSingleField(input)); // Validate on user input
// });

// Validate all fields before form submission
function validateField(form) {
	const inputs = form.querySelectorAll(".acct-input");
	let isValid = true;

	inputs.forEach((input) => {
		if (input.value.trim() === "" || !input.checkValidity()) {
			showErrorMessage(input, getErrorMessage(input));
			isValid = false;
		}
	});

	return isValid;
}

// Get specific error messages based on input validation state
function getErrorMessage(input) {
	if (input.validity.valueMissing) {
		return "This field is required.";
	}
	if (input.validity.typeMismatch) {
		if (input.type === "email") {
			return "Invalid email address.";
		}
		return "Please enter a valid value.";
	}
	if (input.validity.tooShort) {
		return `Please lengthen this text to ${input.minLength} characters or more.`;
	}
	return "Invalid input.";
}

// Show error message below the input
function showErrorMessage(input, msg) {
	let errorMessage = input.nextElementSibling;

	// Create error message element if it doesn't exist
	if (!errorMessage || !errorMessage.classList.contains("error-message")) {
		errorMessage = document.createElement("div");
		errorMessage.className = "error-message";
		input.parentNode.insertBefore(errorMessage, input.nextSibling);
	}

	errorMessage.textContent = msg;
	errorMessage.style.display = "block";
}

// Clear error message when user focuses on the input
function clearErrorMessage(event) {
	const errorMessage = event.target.nextElementSibling;

	if (errorMessage && errorMessage.classList.contains("error-message")) {
		errorMessage.style.display = "none";
	}
}

// Validate a single input field dynamically
function validateSingleField(input) {
	if (input.value.trim() === "" || !input.checkValidity()) {
		showErrorMessage(input, getErrorMessage(input));
	} else {
		clearErrorMessage({ target: input });
	}
}

// Handle form submission
if (submitBtn && acctForm) {
	submitBtn.addEventListener("click", function (e) {
		e.preventDefault(); // Prevent default form submission
		if (validateField(acctForm)) {
			acctForm.submit(); // Submit form only if all inputs are valid
		}
	});
}


// File Upload Script
const fileInfo = document.querySelector(".fileInfo");
const fileInput = document.querySelector("#image_upload");
const fileName = document.querySelector(".fileName");
const fileSize = document.querySelector(".fileSize");
const imgPreview = document.querySelector(".filePreview");

if (document.querySelector(".fileInfo")) {
	fileInput.addEventListener("change", function (event) {
		const file = event.target.files[0];
		if (file) {
			fileInfo.style.display = "flex";

			fileName.textContent = `File Name : ${file.name}`;

			fileSize.textContent = `File Size : ${(file.size / 1024).toFixed(2)}KB`;

			const reader = new FileReader();
			reader.onload = function (e) {
				imgPreview.src = e.target.result;
				imgPreview.style.display = "block";
			};
			reader.readAsDataURL(file);
		}
	});
}

if (document.querySelector(".drop-down-circle.mc-cta")) {
	let dropDownCircle = document.querySelectorAll(".drop-down-circle.mc-cta");

	dropDownCircle.forEach((circle) => {
		circle.addEventListener("click", function (e) {
			let parent = this.closest(".profile-campaigns-container");
			console.log(parent);
			let dropdown = parent.querySelector(".my-campaign.drop-down-cta");

			console.log("hi there");
			let dropdownHeight = dropdown.scrollHeight;
			dropdown.style.setProperty(
				"--dropdown-height",
				`${dropdownHeight + 20}px`
			);
			dropdown.classList.toggle("show");
			this.classList.toggle("active");
		});
	});
}

if (document.querySelector(".my-campaigns.view-more-btn")) {
	const viewMoreBtn = document.querySelectorAll(".my-campaigns.view-more-btn");
	const popup = document.getElementById("popup");
	const closePopup = document.getElementById("close-popup");

	// Show popup on "View More" button click
	viewMoreBtn.forEach((btn) =>
		btn.addEventListener("click", function () {
			console.log(viewMoreBtn);
			popup.classList.add("show");
		})
	);

	// Hide popup on close button click
	closePopup.addEventListener("click", function () {
		popup.classList.remove("show");
	});

	// Hide popup when clicking outside the content
	popup.addEventListener("click", function (event) {
		if (event.target === popup) {
			popup.classList.remove("show");
		}
	});
}

// Search functionaliy

console.log(document.querySelector(".nav-util-cta-container .search-icon-btn"));

if (document.querySelector(".nav-util-cta-container .search-icon-btn")) {
	const items = ["Laptop", "Monitor", "Keyboard", "Mouse", "Headphones"];

	const searchIconBtn = document.querySelector(
		".nav-util-cta-container .search-icon-btn"
	);
	const searchBar = document.querySelector(".search-bar-util-search");
	const searchFuncDiv = document.querySelector(".search-func-div");
	const searchUtilInput = document.querySelector(
		".search-bar-util-search input"
	);

	searchIconBtn.addEventListener("click", () => {
		console.log("Search functioality");
		searchFuncDiv.classList.toggle("reveal");
		setTimeout(() => {
			searchBar.classList.toggle("active");
		}, 500);
	});

	searchUtilInput.addEventListener("input", function () {});
}
