(function () {
  var section = document.getElementById("credentialsSection");
  var btnRequest = document.getElementById("btnRequestCredentials");
  var modalConfirm = document.getElementById("modalConfirmSendCode");
  var modalEnterCode = document.getElementById("modalEnterCode");

  if (!section || !btnRequest) return;

  var documentNumber = (section.getAttribute("data-document") || "").trim();
  var turnstileSiteKey = (section.getAttribute("data-turnstile-key") || "").trim();

  var modalConfirmCancel = document.getElementById("modalConfirmCancel");
  var modalConfirmSend = document.getElementById("modalConfirmSend");
  var confirmSpinner = document.getElementById("confirmSpinner");
  var confirmTurnstileContainer = document.getElementById("confirmTurnstileContainer");
  var confirmErrorPanel = document.getElementById("confirmErrorPanel");
  var confirmErrorText = document.getElementById("confirmErrorText");

  var inputCode = document.getElementById("inputCode");
  var modalCodeErrorPanel = document.getElementById("modalCodeErrorPanel");
  var modalCodeError = document.getElementById("modalCodeError");
  var modalCodeClose = document.getElementById("modalCodeClose");
  var modalCodeValidate = document.getElementById("modalCodeValidate");
  var validateSpinner = document.getElementById("validateSpinner");
  var validateTurnstileContainer = document.getElementById("validateTurnstileContainer");
  var modalCodeForm = document.getElementById("modalCodeForm");
  var modalCodeResult = document.getElementById("modalCodeResult");
  var displayUsuarioPrisma = document.getElementById("displayUsuarioPrisma");
  var displayPasswordPrisma = document.getElementById("displayPasswordPrisma");
  var btnCopyUsuario = document.getElementById("btnCopyUsuario");
  var btnCopyPassword = document.getElementById("btnCopyPassword");
  var modalCodeResultClose = document.getElementById("modalCodeResultClose");
  var codeCountdownContainer = document.getElementById("codeCountdownContainer");
  var codeCountdownDisplay = document.getElementById("codeCountdown");
  var codeBlockHint = document.getElementById("codeBlockHint");

  var confirmTurnstileWidgetId = null;
  var confirmTurnstileToken = null;
  var isSendingCode = false;
  var confirmCountdownContainer = document.getElementById("confirmCountdownContainer");
  var confirmCountdownDisplay = document.getElementById("confirmCountdown");
  var isConfirmBlocked = false;
  var confirmSecondsRemaining = 0;
  var confirmCountdownInterval = null;

  var validateTurnstileWidgetId = null;
  var validateTurnstileToken = null;
  var isValidatingCode = false;

  var isCodeBlocked = false;
  var codeSecondsRemaining = 0;
  var codeCountdownInterval = null;

  function showModal(el) {
    if (el) {
      el.classList.remove("hidden");
      el.classList.add("flex");
      var panel = el.querySelector(".modal-panel");
      if (panel) {
        panel.classList.remove("animate-modal-in");
        panel.offsetHeight;
        panel.classList.add("animate-modal-in");
      }
    }
  }

  function hideModal(el) {
    if (el) {
      el.classList.add("hidden");
      el.classList.remove("flex");
    }
  }

  function showSpinner(spinner, btn) {
    if (spinner) spinner.classList.remove("hidden");
    if (btn) {
      btn.disabled = true;
      btn.classList.add("opacity-70");
    }
  }

  function hideSpinner(spinner, btn) {
    if (spinner) spinner.classList.add("hidden");
    if (btn) {
      btn.disabled = false;
      btn.classList.remove("opacity-70");
    }
  }

  function showConfirmError(message) {
    if (confirmErrorText) confirmErrorText.textContent = message;
    if (confirmErrorPanel) confirmErrorPanel.classList.remove("hidden");
  }

  function hideConfirmError() {
    if (confirmErrorPanel) confirmErrorPanel.classList.add("hidden");
    hideConfirmCountdown();
  }

  function lockConfirmButton() {
    isConfirmBlocked = true;
    if (modalConfirmSend) {
      modalConfirmSend.disabled = true;
      modalConfirmSend.classList.add("opacity-50", "cursor-not-allowed");
    }
  }

  function unlockConfirmButton() {
    isConfirmBlocked = false;
    confirmSecondsRemaining = 0;
    if (confirmCountdownInterval) {
      clearInterval(confirmCountdownInterval);
      confirmCountdownInterval = null;
    }
    if (modalConfirmSend) {
      modalConfirmSend.disabled = false;
      modalConfirmSend.classList.remove("opacity-50", "cursor-not-allowed");
    }
    hideConfirmError();
  }

  function showConfirmCountdown(seconds) {
    confirmSecondsRemaining = seconds;
    lockConfirmButton();
    if (confirmCountdownContainer) confirmCountdownContainer.classList.remove("hidden");
    if (confirmCountdownDisplay) confirmCountdownDisplay.textContent = formatTime(confirmSecondsRemaining);
    if (confirmCountdownInterval) clearInterval(confirmCountdownInterval);
    confirmCountdownInterval = setInterval(function() {
      confirmSecondsRemaining--;
      if (confirmSecondsRemaining <= 0) {
        unlockConfirmButton();
      } else if (confirmCountdownDisplay) {
        confirmCountdownDisplay.textContent = formatTime(confirmSecondsRemaining);
      }
    }, 1000);
  }

  function hideConfirmCountdown() {
    if (confirmCountdownContainer) confirmCountdownContainer.classList.add("hidden");
    if (confirmCountdownInterval) {
      clearInterval(confirmCountdownInterval);
      confirmCountdownInterval = null;
    }
  }

  function showCodeError(message) {
    if (modalCodeError) modalCodeError.textContent = message;
    if (modalCodeErrorPanel) modalCodeErrorPanel.classList.remove("hidden");
  }

  function hideCodeError() {
    if (modalCodeErrorPanel) modalCodeErrorPanel.classList.add("hidden");
    hideCodeCountdown();
  }

  function formatTime(totalSeconds) {
    var minutes = Math.floor(totalSeconds / 60);
    var seconds = totalSeconds % 60;
    return String(minutes).padStart(2, "0") + ":" + String(seconds).padStart(2, "0");
  }

  function lockCodeInput() {
    isCodeBlocked = true;
    if (inputCode) {
      inputCode.disabled = true;
      inputCode.classList.add("opacity-50", "cursor-not-allowed");
    }
    if (modalCodeValidate) {
      modalCodeValidate.disabled = true;
      modalCodeValidate.classList.add("opacity-50", "cursor-not-allowed");
    }
  }

  function unlockCodeInput() {
    isCodeBlocked = false;
    codeSecondsRemaining = 0;
    if (codeCountdownInterval) {
      clearInterval(codeCountdownInterval);
      codeCountdownInterval = null;
    }
    if (inputCode) {
      inputCode.disabled = false;
      inputCode.classList.remove("opacity-50", "cursor-not-allowed");
    }
    if (modalCodeValidate) {
      modalCodeValidate.disabled = false;
      modalCodeValidate.classList.remove("opacity-50", "cursor-not-allowed");
    }
    hideCodeError();
  }

  function showCodeCountdown(seconds) {
    codeSecondsRemaining = seconds;
    lockCodeInput();
    if (codeBlockHint) codeBlockHint.classList.remove("hidden");
    if (codeCountdownContainer) codeCountdownContainer.classList.remove("hidden");
    if (codeCountdownDisplay) codeCountdownDisplay.textContent = formatTime(codeSecondsRemaining);
    if (codeCountdownInterval) clearInterval(codeCountdownInterval);
    codeCountdownInterval = setInterval(function() {
      codeSecondsRemaining--;
      if (codeSecondsRemaining <= 0) {
        unlockCodeInput();
      } else if (codeCountdownDisplay) {
        codeCountdownDisplay.textContent = formatTime(codeSecondsRemaining);
      }
    }, 1000);
  }

  function hideCodeCountdown() {
    if (codeCountdownContainer) codeCountdownContainer.classList.add("hidden");
    if (codeBlockHint) codeBlockHint.classList.add("hidden");
    if (codeCountdownInterval) {
      clearInterval(codeCountdownInterval);
      codeCountdownInterval = null;
    }
  }

  function copyToClipboard(text, btn) {
    if (!navigator.clipboard) return;
    navigator.clipboard.writeText(text).then(function () {
      var originalHTML = btn.innerHTML;
      btn.innerHTML =
        '<svg class="w-4 h-4 text-[#39A900]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>';
      setTimeout(function () {
        btn.innerHTML = originalHTML;
      }, 1500);
    });
  }

  function loadTurnstileScript(callback) {
    if (window.turnstile) {
      callback();
      return;
    }
    var script = document.createElement("script");
    script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js";
    script.async = true;
    script.onload = function () {
      callback();
    };
    document.body.appendChild(script);
  }

  function destroyConfirmTurnstile() {
    if (window.turnstile && confirmTurnstileWidgetId !== null) {
      try { turnstile.remove(confirmTurnstileWidgetId); } catch (e) {}
    }
    confirmTurnstileWidgetId = null;
    confirmTurnstileToken = null;
    if (confirmTurnstileContainer) {
      confirmTurnstileContainer.innerHTML = "";
      confirmTurnstileContainer.classList.add("hidden");
    }
  }

  function destroyValidateTurnstile() {
    if (window.turnstile && validateTurnstileWidgetId !== null) {
      try { turnstile.remove(validateTurnstileWidgetId); } catch (e) {}
    }
    validateTurnstileWidgetId = null;
    validateTurnstileToken = null;
    if (validateTurnstileContainer) {
      validateTurnstileContainer.innerHTML = "";
      validateTurnstileContainer.classList.add("hidden");
    }
  }

  function renderConfirmTurnstile() {
    if (!confirmTurnstileContainer || !window.turnstile) return;
    destroyConfirmTurnstile();
    confirmTurnstileContainer.classList.remove("hidden");
    confirmTurnstileWidgetId = turnstile.render(confirmTurnstileContainer, {
      sitekey: turnstileSiteKey,
      theme: "light",
      callback: function (token) {
        confirmTurnstileToken = token;
        doSendCode();
      },
      "error-callback": function () {
        destroyConfirmTurnstile();
        hideSpinner(confirmSpinner, modalConfirmSend);
        showConfirmError("Error en la verificación de seguridad. Inténtalo de nuevo.");
      },
      "expired-callback": function () {
        confirmTurnstileToken = null;
      },
    });
  }

  function renderValidateTurnstile() {
    if (!validateTurnstileContainer || !window.turnstile) return;
    destroyValidateTurnstile();
    validateTurnstileContainer.classList.remove("hidden");
    validateTurnstileWidgetId = turnstile.render(validateTurnstileContainer, {
      sitekey: turnstileSiteKey,
      theme: "light",
      callback: function (token) {
        validateTurnstileToken = token;
        doValidateRequest();
      },
      "error-callback": function () {
        destroyValidateTurnstile();
        hideSpinner(validateSpinner, modalCodeValidate);
        showCodeError("Error en la verificación de seguridad. Intenta de nuevo.");
      },
      "expired-callback": function () {
        validateTurnstileToken = null;
      },
    });
  }

  var noHabilitadoMessage = document.getElementById("noHabilitadoMessage");

  btnRequest.addEventListener("click", function () {
    var estadoConvocatoria = (section.getAttribute("data-estado-convocatoria") || "").toUpperCase().trim();
    if (estadoConvocatoria === "NO HABILITADO") {
      if (noHabilitadoMessage) {
        noHabilitadoMessage.classList.remove("hidden");
        noHabilitadoMessage.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      return;
    }
    destroyConfirmTurnstile();
    isConfirmBlocked = false;
    if (confirmCountdownInterval) {
      clearInterval(confirmCountdownInterval);
      confirmCountdownInterval = null;
    }
    if (modalConfirmSend) {
      modalConfirmSend.disabled = false;
      modalConfirmSend.classList.remove("opacity-50", "cursor-not-allowed");
    }
    hideConfirmError();
    isSendingCode = false;
    showModal(modalConfirm);
  });

  modalConfirmCancel.addEventListener("click", function () {
    destroyConfirmTurnstile();
    unlockConfirmButton();
    hideModal(modalConfirm);
  });

  function doSendCode() {
    if (isSendingCode) return;
    isSendingCode = true;
    hideConfirmError();
    showSpinner(confirmSpinner, modalConfirmSend);
    var body = { document: documentNumber };
    if (confirmTurnstileToken) {
      body["cf-turnstile-response"] = confirmTurnstileToken;
    }
    fetch("/users/credentials/send-code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, status: res.status, data: data };
        });
      })
      .then(function (result) {
        hideSpinner(confirmSpinner, modalConfirmSend);
        destroyConfirmTurnstile();
        isSendingCode = false;
        if (result.ok && result.data.success) {
          hideModal(modalConfirm);
          hideCodeError();
          unlockCodeInput();
          destroyValidateTurnstile();
          modalCodeForm.classList.remove("hidden");
          modalCodeResult.classList.add("hidden");
          inputCode.value = "";
          showModal(modalEnterCode);
        } else {
          showConfirmError(result.data.message || "No se pudo enviar el código.");
          if (result.data.blocked && result.data.seconds_remaining) {
            showConfirmCountdown(result.data.seconds_remaining);
          }
        }
      })
      .catch(function () {
        hideSpinner(confirmSpinner, modalConfirmSend);
        destroyConfirmTurnstile();
        isSendingCode = false;
        showConfirmError("Error de conexión. Inténtalo de nuevo.");
      });
  }

  modalConfirmSend.addEventListener("click", function () {
    if (isConfirmBlocked || isSendingCode) return;
    hideConfirmError();
    if (turnstileSiteKey) {
      loadTurnstileScript(function () {
        renderConfirmTurnstile();
      });
      return;
    }
    doSendCode();
  });

  modalCodeClose.addEventListener("click", function () {
    destroyValidateTurnstile();
    unlockCodeInput();
    hideModal(modalEnterCode);
  });

  function doValidateRequest() {
    hideCodeError();
    showSpinner(validateSpinner, modalCodeValidate);
    var code = (inputCode.value || "").trim();
    var body = { document: documentNumber, code: code };
    if (validateTurnstileToken) {
      body["cf-turnstile-response"] = validateTurnstileToken;
    }
    fetch("/users/credentials/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        });
      })
      .then(function (result) {
        hideSpinner(validateSpinner, modalCodeValidate);
        destroyValidateTurnstile();
        isValidatingCode = false;
        if (result.data.success) {
          var usuarioPrisma = (result.data.usuario_prisma || "").trim();
          var passwordPrisma = (result.data.password_prisma || "").trim();
          displayUsuarioPrisma.textContent = usuarioPrisma ? usuarioPrisma : "No cuenta";
          displayPasswordPrisma.textContent = passwordPrisma ? passwordPrisma : "No cuenta";
          modalCodeForm.classList.add("hidden");
          modalCodeResult.classList.remove("hidden");
        } else {
          showCodeError(result.data.message || "Código incorrecto.");
          if (result.data.blocked && result.data.seconds_remaining) {
            showCodeCountdown(result.data.seconds_remaining);
          }
        }
      })
      .catch(function () {
        hideSpinner(validateSpinner, modalCodeValidate);
        destroyValidateTurnstile();
        isValidatingCode = false;
        showCodeError("Error de conexión.");
      });
  }

  function doValidate() {
    if (isCodeBlocked) return;
    var code = (inputCode.value || "").trim();
    if (!code) {
      showCodeError("Ingresa el código.");
      return;
    }
    if (isValidatingCode) return;
    isValidatingCode = true;
    hideCodeError();
    if (turnstileSiteKey) {
      loadTurnstileScript(function () {
        renderValidateTurnstile();
      });
      return;
    }
    doValidateRequest();
  }

  modalCodeValidate.addEventListener("click", doValidate);
  inputCode.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      doValidate();
    }
  });
  inputCode.addEventListener("input", function () {
    var value = inputCode.value.toUpperCase().replace(/[^A-Z0-9]/g, "");
    if (value.length > 6) {
      value = value.substring(0, 6);
    }
    inputCode.value = value;
  });

  if (btnCopyUsuario) {
    btnCopyUsuario.addEventListener("click", function () {
      copyToClipboard(displayUsuarioPrisma.textContent, btnCopyUsuario);
    });
  }
  if (btnCopyPassword) {
    btnCopyPassword.addEventListener("click", function () {
      copyToClipboard(displayPasswordPrisma.textContent, btnCopyPassword);
    });
  }

  modalCodeResultClose.addEventListener("click", function () {
    hideModal(modalEnterCode);
  });
})();
