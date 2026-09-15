# Release v0.3.0 - 2026-09-15

## What's new

### Admin products menu
- Combined separate product edit, delete and statistics functions in one under product info menu
- Added admin catalog view
- Added product info menu with built-in product editing and deletion

## Improvements & Changes
- Renamed "Products" to "Catalog" across the entire interface for clarity
- Slightly improved code structure

## Bug fixes
- Fixed an issue where admin request responses were occasionally miscounted as user responses 
- Various fixes with Finite State Machine (FSM) state transitions

# Patch v0.2.1 - 2026-09-15

## What's new

### Changelog
- Added timestamps to all logs for better tracking

## Bug fixes
- Fixed an issue where the displayed bot version did not match the actual release version

# Release v0.2.0 - 2026-09-13

## What's new

### Design
- Changed bot's overall visual design

### Support system
- Added admin/user support request notifications
- Added support conversation history
- Added user/admin replies
- Added request pagination

### User support menu
- Improved "Make a support request" section
- Added "My Requests" section

### Database
- Divided one support_requests table into support_requests and support_messages tables
- Added user/request relationships

## Other
- Improved error handling
- Fixed minor README.md mistakes