.. automodule:: uge.api

.. currentmodule:: uge.api

QconfApi
--------

.. autoclass:: uge.api.QconfApi()
    :members: __init__,
              get_uge_version, generate_object,
              generate_acl, add_acl, modify_acl, 
              get_acl, delete_acl, list_acls, 
              add_users_to_acls,
              delete_users_from_acls,
              add_ahosts, delete_ahosts, list_ahosts,
              generate_cal, add_cal, modify_cal, 
              get_cal, delete_cal, list_cals, 
              generate_ckpt, add_ckpt, modify_ckpt,
              get_ckpt, delete_ckpt, list_ckpts, 
              generate_cconf, get_cconf, modify_cconf, 
              add_cattr, modify_cattr, delete_cattr,
              generate_conf, add_conf, modify_conf, 
              get_conf, delete_conf, list_confs, 
              generate_ehost, add_ehost, modify_ehost, 
              get_ehost, delete_ehost, list_ehosts, 
              generate_hgrp, add_hgrp, modify_hgrp, 
              get_hgrp, delete_hgrp, list_hgrps, 
              generate_jc, add_jc, modify_jc, 
              get_jc, delete_jc, list_jcs, 
              add_managers, delete_managers, list_managers,
              add_operators, delete_operators, list_operators,
              generate_pe, add_pe, modify_pe,
              get_pe, delete_pe, list_pes, 
              generate_prj, add_prj, modify_prj, 
              get_prj, delete_prj, list_prjs, 
              generate_queue, add_queue, modify_queue,
              get_queue, delete_queue, list_queues, 
              generate_rqs, add_rqs, modify_rqs, 
              get_rqs, delete_rqs, list_rqss, 
              generate_sconf, modify_sconf, 
              get_sconf,
              generate_stree, add_stree, modify_stree, modify_or_add_stree, 
              get_stree, get_stree_if_exists, 
              delete_stree, delete_stree_if_exists,
              add_stnode, delete_stnode,
              generate_user, add_user, modify_user, 
              get_user, delete_user, list_users, 
              add_shosts, delete_shosts, list_shosts
    :show-inheritance:

AdvanceReservationApi
---------------------

.. autoclass:: uge.api.AdvanceReservationApi()
    :members: __init__,
              get_uge_version, get_ar, get_ar_summary,
              get_ar_list, request_ar, delete_ar
    :show-inheritance:

