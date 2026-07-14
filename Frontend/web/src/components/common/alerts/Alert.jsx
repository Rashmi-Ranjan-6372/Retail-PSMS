import {
  Alert as ChakraAlert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from "@chakra-ui/react";

import {
  successAlert,
  errorAlert,
  warningAlert,
  infoAlert,
  alertTitle,
  alertDescription,
} from "../../../styles/components/alerts";

const variants = {
  success: successAlert,
  error: errorAlert,
  warning: warningAlert,
  info: infoAlert,
};

const Alert = ({
  status = "info",
  title,
  children,
  icon = true,
  sx = {},
  ...props
}) => {
  return (
    <ChakraAlert
      status={status}
      sx={{
        ...(variants[status] || infoAlert),
        ...sx,
      }}
      {...props}
    >
      {icon && <AlertIcon />}

      <div>
        {title && <AlertTitle sx={alertTitle}>{title}</AlertTitle>}

        {children && (
          <AlertDescription sx={alertDescription}>{children}</AlertDescription>
        )}
      </div>
    </ChakraAlert>
  );
};

export default Alert;
