import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Text,
} from "@chakra-ui/react";
import { ChevronRightIcon } from "@chakra-ui/icons";
import { Link, useLocation } from "react-router-dom";

import { colors } from "../../../styles/common/colors";

const Breadcrumbs = () => {
  const location = useLocation();

  const pathnames = location.pathname.split("/").filter(Boolean);

  return (
    <Breadcrumb
      spacing="8px"
      separator={<ChevronRightIcon color={colors.textMuted} />}
      mb={6}
    >
      <BreadcrumbItem>
        <BreadcrumbLink
          as={Link}
          to="/"
          color={colors.primary}
          fontWeight="600"
        >
          Home
        </BreadcrumbLink>
      </BreadcrumbItem>

      {pathnames.map((segment, index) => {
        const route = `/${pathnames.slice(0, index + 1).join("/")}`;

        const isCurrent = index === pathnames.length - 1;

        const label = segment
          .replace(/-/g, " ")
          .replace(/\b\w/g, (char) => char.toUpperCase());

        return (
          <BreadcrumbItem key={route} isCurrentPage={isCurrent}>
            {isCurrent ? (
              <Text color={colors.textPrimary} fontWeight="600">
                {label}
              </Text>
            ) : (
              <BreadcrumbLink as={Link} to={route} color={colors.textSecondary}>
                {label}
              </BreadcrumbLink>
            )}
          </BreadcrumbItem>
        );
      })}
    </Breadcrumb>
  );
};

export default Breadcrumbs;
