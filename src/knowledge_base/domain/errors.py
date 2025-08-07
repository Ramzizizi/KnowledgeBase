################################## MAIN ERROR ##################################
class DomainError(Exception): ...


################################ DOMAINS ERRORS ################################
class NotFound(DomainError): ...


class HasRelatedData(DomainError): ...


############################# VALUE OBJECTS ERRORS #############################


class InvalidValue(ValueError): ...
