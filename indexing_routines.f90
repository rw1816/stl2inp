! subroutine to index elements from nodal coordinates
! compiled by f2py, outputting a .pyd file which is then called from a wrapper python script
!-----------------------------------------------------------------------------
!
!the comment lines below beginning with !f2py, inputs: and outputs: are special comments
!read by the compiler, or the wrapper (not sure which) so MUST be retained and correct
!-----------------------------------------------------------------------------
! RJW, Imperial College London, Aug 2020 
!
!

SUBROUTINE index_els(x, y, z, node_num, scale_factor, length, els_out, INC)
    ! Inputs: x, y, z, node_num, scale_factor
    ! Output: els_out.

    integer, dimension(length) :: x, y, z, node_num
    integer :: current_node(3)
    integer, dimension(8) :: current_element != (/ 0, 0, 0, 0, 0, 0, 0, 0 /)
    integer, dimension(length, 8) :: els_out  !do I need to declare all variables in the f2py section under (hide)
    REAL :: scale_factor
    REAL :: INC
    
    !f2py intent(in) :: x, y, z, node_num, scale_factor
    !f2py intent(hide), depend(length) :: length = shape(x,0)
    !f2py intent(out) :: els_out, INC
    
    INC = 1.0/scale_factor

!now start doing the actual programming
    DO j=1,length
        
        current_node(1) = x(j)
        current_node(2) = y(j)
        current_node(3) = z(j)
        
        DO i=1,length
        
            IF (x(i)==current_node(1).AND.y(i)==current_node(2).AND.z(i)==current_node(3)) THEN  !i.e. we are at our node
                current_element(1) = node_num(i)
                
            END IF
            
            IF (x(i)==(current_node(1)+INC).AND.y(i)==current_node(2).AND.z(i)==current_node(3)) THEN  !i.e. we are at node 2
                current_element(2) = node_num(i)
                
            END IF
            
            IF (x(i)==(current_node(1)+INC).AND.y(i)==current_node(2).AND.z(i)==current_node(3)) THEN  !i.e. we are at node 2
                current_element(2) = node_num(i)
                
            END IF
            
            IF (x(i)==(current_node(1)+INC).AND.(y(i)==(current_node(2)+INC)).AND.(z(i)==current_node(3))) THEN  !i.e. we are at node 3
                current_element(3) = node_num(i)
                
            END IF
            
            IF (x(i)==current_node(1).AND.y(i)==(current_node(2)+INC).AND.z(i)==current_node(3)) THEN  !i.e. we are at node 4
                current_element(4) = node_num(i)
                
            END IF
            
            IF (x(i)==current_node(1).AND.y(i)==current_node(2).AND.z(i)==(current_node(3)+INC)) THEN  !i.e. we are at node 5
                current_element(5) = node_num(i)
                
            END IF
            
            IF (x(i)==(current_node(1)+INC).AND.y(i)==current_node(2).AND.z(i)==(current_node(3)+INC)) THEN  !i.e. we are at node 6
                current_element(6) = node_num(i)
                
            END IF
            
            IF (x(i)==(current_node(1)+INC).AND.y(i)==(current_node(2)+INC).AND.z(i)==(current_node(3)+INC)) THEN  !i.e. we are at node 7
                current_element(7) = node_num(i)
                
            END IF
            
            IF (x(i)==current_node(1).AND.y(i)==(current_node(2)+INC).AND.z(i)==(current_node(3)+INC)) THEN  !i.e. we are at node 8
                current_element(8) = node_num(i)
                
            END IF
            
        END DO
        
        IF (ANY(current_element == 0)) THEN
            
            els_out(j,1:8) = 0
            
        ELSE 
        
            els_out(j,1:8) = current_element(1:8)
            
        END IF
        
        current_element(1:8)=0
        
    END DO
        
END SUBROUTINE

!! ********************************* Routine to write out all 8 nodes from element centroid **************************************************


SUBROUTINE write_nodes(centroids_all, num_voxels, nodes_all)
    ! Inputs centroids_all, num_voxels
    ! Outputs nodes_all 
    !
    
    integer :: num_voxels, counter
    real, dimension(num_voxels, 3) :: centroids_all
    real, dimension(3) :: subtract, node_inc1, node_inc2, node_inc3, node_inc4, node_inc5, node_inc6, node_inc7
    real, dimension((num_voxels*8), 3) :: nodes_all  !do I need to declare all variables in the f2py section under (hide)
    
    !f2py intent(in) :: centroids_all, num_voxels
    !f2py intent(hide) :: counter
    !f2py intent(out) :: nodes_all
    
    !now start doing the actual programming
    counter = 1
    subtract = (/0.5, 0.5, 0.5/)
    node_inc1 = (/1.0, 0.0, 0.0/)
    node_inc2 = (/0.0, 1.0, 0.0/)
    node_inc3 = (/0.0, 0.0, 1.0/)
    node_inc4 = (/1.0, 1.0, 0.0/)
    node_inc5 = (/1.0, 0.0, 1.0/)
    node_inc6 = (/0.0, 1.0, 1.0/)
    node_inc7 = (/1.0, 1.0, 1.0/)
    
    DO i=1, num_voxels
        
        nodes_all(counter, :) = centroids_all(i, :) - subtract
        counter = counter + 1 
        
        nodes_all(counter, :) = centroids_all(i, :) - subtract + node_inc1
        counter = counter + 1 
        
        nodes_all(counter, :) = centroids_all(i, :) - subtract + node_inc2
        counter = counter + 1 
        
        nodes_all(counter, :) = centroids_all(i, :) - subtract + node_inc3
        counter = counter + 1 
        
        nodes_all(counter, :) = centroids_all(i, :) - subtract + node_inc4
        counter = counter + 1
        
        nodes_all(counter, :) = centroids_all(i, :) - subtract + node_inc5
        counter = counter + 1
        
        nodes_all(counter, :) = centroids_all(i, :) - subtract + node_inc6
        counter = counter + 1
        
        nodes_all(counter, :) = centroids_all(i, :) - subtract + node_inc7
        counter = counter + 1
        
    END DO
    
END SUBROUTINE