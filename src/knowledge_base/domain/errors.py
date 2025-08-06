################################## MAIN ERROR ##################################
class DomainError(Exception): ...


################################# PATCH ERROR ##################################
class InvalidPatch(DomainError): ...


################################ DOMAINS ERRORS ################################
class CategoryNotFound(DomainError): ...


class SubCategoryNotFound(DomainError): ...


class TaskNotFound(DomainError): ...


class QuestionNotFound(DomainError): ...


class SourceNotFound(DomainError): ...


class CategoryHasRelatedData(DomainError): ...


class SubCategoryHasRelatedData(DomainError): ...


############################# VALUE OBJECTS ERRORS #############################


class InvalidTitle(ValueError): ...


class InvalidId(ValueError): ...


class InvalidLink(ValueError): ...
