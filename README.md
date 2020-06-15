# metadata_mongo_ingester
    Provide APIs to validate metadata documents against a schema and ingest them into a MongoDB collection.

   

## Overview
   The microscopy data manager runs a scan each morning of the microscopy delivery folders, located on jax window shares (see [Configuration and target directories](https://github.com/TheJacksonLaboratory/microscopy_data_mgmt/blob/master/README.md#configuration-and-target-directories), below). It sends an e-mail noting which folders have data, metadata, have been archived, are older or newer than 90 days, and which can or must be deleted. It also notes any serious problems encountered, such as folder contents being altered after archiving has occurred. In future versions, it will archive and delete the data as needed.

## Documentation
The subjects below are documented in more detail in the [docs](https://github.com/TheJacksonLaboratory/metadata_mongo_ingester/tree/master/docs) folder.

### Run Environment
The [Run Environment](https://github.com/TheJacksonLaboratory/microscopy_data_mgmt/blob/master/docs/Run%20environment.md) page describes the server and service account to use, the daily cron job, job scripts, and log files.

### Class Structure and Control Flow
The [Class Structure and Control Flow](https://github.com/TheJacksonLaboratory/microscopy_data_mgmt/blob/master/docs/Class%20structure%20and%20control%20flow.md) page explains what the different classes do and how they work together.

### Unit Tests
The [Unit tests](https://github.com/TheJacksonLaboratory/microscopy_data_mgmt/blob/master/docs/Unit%20tests.md) details the structure of the unit tests. 

## Questions?
Please contact [Neil Kindlon](mailto:Neil.Kindlon@jax.org) or [Dave Mellert](mailto:Dave.Mellert@jax.org) in the [Research IT](https://jacksonlaboratory.sharepoint.com/sites/ResearchIT) [Research Solutions Team](https://jacksonlaboratory.sharepoint.com/sites/ResearchIT/SitePages/Research-Solutions.aspx) for assistance.
