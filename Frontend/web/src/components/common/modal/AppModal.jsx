import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalCloseButton,
} from "@chakra-ui/react";

import {
  modalOverlay,
  modalContent,
  modalHeader,
  modalBody,
  modalFooter,
  modalCloseButton,
} from "../../../styles/components/modal";

const AppModal = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = "lg",
  closeOnOverlayClick = false,
}) => {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size={size}
      isCentered
      closeOnOverlayClick={closeOnOverlayClick}
    >
      <ModalOverlay sx={modalOverlay} />

      <ModalContent sx={modalContent}>
        <ModalHeader sx={modalHeader}>{title}</ModalHeader>

        <ModalCloseButton sx={modalCloseButton} />

        <ModalBody sx={modalBody}>{children}</ModalBody>

        {footer && <ModalFooter sx={modalFooter}>{footer}</ModalFooter>}
      </ModalContent>
    </Modal>
  );
};

export default AppModal;
