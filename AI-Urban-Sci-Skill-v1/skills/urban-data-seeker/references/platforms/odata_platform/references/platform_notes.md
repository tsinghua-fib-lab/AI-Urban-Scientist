# OData Platform Notes

OData services expose a service document, `$metadata`, entity sets, and query options such as `$top`, `$select`, `$filter`, `$orderby`, and `$format`. Public-data APIs may implement different OData versions and subsets.

This platform package only builds route-ready hints:

- service document;
- metadata document;
- capped entity-set query templates.

It does not know the domain meaning of an entity set. A SourceSkill or route runner must validate metadata, entity-set names, fields, filters, paging, service version, and response format before any probe or acquisition.

## References

- OData basic tutorial: https://www.odata.org/getting-started/basic-tutorial/
- OData 4.01 protocol specification: https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html
- OData v2 URI conventions and system query options: https://www.odata.org/documentation/odata-version-2-0/uri-conventions/
