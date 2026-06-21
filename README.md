# Auth Licence

A simple authentication system with role-based access control.

## Usage

1. Create an instance of `AuthLicence`.
2. Sign up a user with a role using `signup`.
3. Call an endpoint using `call_endpoint`.

## Endpoints

* `free_endpoint`: Available to users with the `FREE` role.
* `pro_endpoint`: Available to users with the `PRO` role.
* `admin_endpoint`: Available to users with the `ADMIN` role.
