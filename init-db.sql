DO $$
BEGIN
    -- Create genre_enum if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'genre_enum') THEN
        CREATE TYPE genre_enum AS ENUM (
            'PROGRAMMING_LANGUAGES',
            'DESIGN_PATTERNS', 
            'SOFTWARE_ARCHITECTURE', 
            'DEVOPS', 
            'SOFTWARE_TESTING', 
            'PROJECT_MANAGEMENT', 
            'USER_EXPERIENCE', 
            'SECURITY'
        );
    END IF;

    -- Create condition_enum if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'condition_enum') THEN
        CREATE TYPE condition_enum AS ENUM (
            'FACTORY_NEW',
            'MINIMAL_WEAR',
            'FIELD_TESTED',
            'WELL_WORN',
            'BATTLE_SCARRED'
        );
    END IF;

    -- Create availability_enum if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'availability_enum') THEN
        CREATE TYPE availability_enum AS ENUM (
            'AVAILABLE',
            'UNAVAILABLE',
            'RESERVED'
        );
    END IF;

    -- Create borrow_status_enum if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'borrow_status_enum') THEN
        CREATE TYPE borrow_status_enum AS ENUM (
            'PENDING',
            'APPROVED',
            'REJECTED',
            'BORROWED',
            'RETURNED'
        );
    END IF;
END
$$;