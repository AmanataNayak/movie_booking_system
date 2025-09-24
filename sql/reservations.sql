CREATE TABLE reservations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL, -- from auth_service
    showtime_id UUID NOT NULL, -- from catalog_service.showtimes
    status VARCHAR(20) NOT NULL CHECK (status IN ('hold', 'confirmed', 'cancelled', 'expired')),
    created_at TIMESTAMPT DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
);


CREATE TABLE reserved_seats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id UUID NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
    seat_id UUID NOT NULL, -- from catalog_service.seats
    UNIQUE (seat_id, reservation_id)
);