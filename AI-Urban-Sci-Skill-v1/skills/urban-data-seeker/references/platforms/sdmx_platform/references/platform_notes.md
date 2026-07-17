# SDMX Platform Notes

SDMX is a family of statistical data-exchange APIs used by organizations such as OECD, Eurostat, IMF, World Bank SDMX endpoints, and national statistical offices. Implementations differ across SDMX REST versions and provider conventions.

This platform package only builds route-ready hints:

- dataflow metadata;
- data-query templates using dataflow and series key inputs.

It does not resolve provider-specific dimensions by itself. A SourceSkill or route runner must validate the real dataflow, data structure definition, dimensions, codelists, time period filters, content negotiation, and provider-specific SDMX version before probe or acquisition.

## References

- SDMX standards page: https://sdmx.org/standards-2/
- SDMX REST API specifications: https://github.com/sdmx-twg/sdmx-rest
- SDMX 2.1 web services guidelines: https://sdmx.org/wp-content/uploads/SDMX_2-1-1-SECTION_07_WebServicesGuidelines_2013-04.pdf
