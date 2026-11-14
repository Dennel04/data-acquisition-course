// Tartu Narva College / Andmehõive Labor 3
// TILGAPLAAT v1 — print-ready plate (not physically validated).
// 25 VIRTUAL droplet positions: an entirely FLAT working zone, NO HOLES.
// Read positions by intersection of numbered top columns and lettered right rows.
// Dimensional proposal, not physical data: verify maximal resin spot diameter!
// Render STL in OpenSCAD with F6, then File -> Export -> Export as STL.

plate_size = 80;           // mm
plate_thickness = 2.4;     // mm
corner_radius = 1.5;      // mm
pitch = 12;               // mm, MUST validate after first real droplet test
rows = 5;
columns = 5;
engrave_depth = 0.40;     // mm, two or three 0.2 mm layers
mark_width = 0.75;        // mm
ruler_line_width = 0.50;  // mm
label_size = 3.1;         // mm
$fn = 48;

function x_col(c) = plate_size/2 + (c-2)*pitch;
function y_row(r) = plate_size/2 + (2-r)*pitch;

module rounded_plate() {
    linear_extrude(height=plate_thickness)
        offset(r=corner_radius)
            translate([corner_radius,corner_radius])
                square([plate_size-2*corner_radius,plate_size-2*corner_radius]);
}
module engraved_text(s,x,y,size=label_size) {
    translate([x,y,plate_thickness-engrave_depth])
        linear_extrude(height=engrave_depth+0.08)
            text(s,size=size,font="Liberation Sans:style=Bold",halign="center",valign="center");
}
module engraved_rect(x,y,w,h) {
    translate([x,y,plate_thickness-engrave_depth])
        cube([w,h,engrave_depth+0.08]);
}
module all_marks() {
    // Top labels 1–5. Tiny ticks project into the BORDER, not droplet area.
    for(c=[0:columns-1]) {
        engraved_text(str(c+1),x_col(c),74,3.4);
        engraved_rect(x_col(c)-mark_width/2,68.4,mark_width,2.2);
    }
    // Right labels A–E. No interruptions of the central 5x5 drop surface.
    for(r=[0:rows-1]) {
        engraved_text(chr(65+r),74,y_row(r),3.4);
        engraved_rect(68.4,y_row(r)-mark_width/2,2.2,mark_width);
    }
    // Rulers along bottom and left: positions 10..70 mm at 2 mm intervals.
    // Larger marks every 10 mm; labels show millimetres from the 10 mm origin.
    for(t=[0:30]) {
        p=10+2*t;
        major=(t%5==0);
        len=major?4.0:2.0;
        engraved_rect(p-ruler_line_width/2,1.6,ruler_line_width,len);
        engraved_rect(1.6,p-ruler_line_width/2,len,ruler_line_width);
    }
    // Orientation marker in top-left, NOT a through-hole.
    translate([6.8,73,plate_thickness-engrave_depth])
        linear_extrude(height=engrave_depth+0.08)
            polygon(points=[[-1.6,-1.2],[1.6,-1.2],[0,1.8]]);
}

difference(){ rounded_plate(); all_marks(); }
