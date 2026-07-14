import { Button } from "@chakra-ui/react";

import AppModal from "./AppModal";

import {
  primaryButton,
  secondaryButton,
} from "../../../styles/components/buttons";

const ConfirmModal = ({
  isOpen,
  onClose,
  onConfirm,
  title = "Confirmation",
  message = "Are you sure?",
  confirmText = "Confirm",
  cancelText = "Cancel",
  isLoading = false,
}) => {
  const footer = (
    <>
      <Button sx={secondaryButton} mr={3} onClick={onClose}>
        {cancelText}
      </Button>

      <Button sx={primaryButton} onClick={onConfirm} isLoading={isLoading}>
        {confirmText}
      </Button>
    </>
  );

  return (
    <AppModal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      footer={footer}
      size="md"
    >
      {message}
    </AppModal>
  );
};

export default ConfirmModal;
