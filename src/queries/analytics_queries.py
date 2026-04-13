OUT_STANDING_BALANCE_QUERY =  '''
                              WITH extract_data_purchase AS
                              (
                                   SELECT
                                        seller_id,
                                        SUM((((total_bags * 30) - waste_pieces) * rate_per_piece)) AS total_purchase
                                   FROM finance.purchases
                                   GROUP BY
                                        seller_id
                              ),
                                   extract_data_payment AS
                              (
                                   SELECT 
                                        seller_id,
                                        SUM(amount_paid) AS total_amount_paid
                                   FROM finance.paymentS
                                   GROUP BY
                                        seller_id
                              )
                              SELECT
                                   s.seller_id,
                                   s.seller_name,
                                   COALESCE(pur.total_purchase, 0) AS total_purchase,
                                   COALESCE(pay.total_amount_paid,0) AS total_amount_paid,
                                   COALESCE((pur.total_purchase - pay.total_amount_paid), 0) AS  outstanding_balance
                              FROM master.sellers s
                              LEFT JOIN extract_data_purchase pur
                                   ON s.seller_id = pur.seller_id
                              LEFT JOIN extract_data_payment pay
                                   ON pay.seller_id = pur.seller_id
                              '''

YEARLY_PURCHASE_QUERY    =    '''
                              WITH extract_data AS
                              (
                                   SELECT 
                                        seller_id,
                                        TO_CHAR(purchase_date, 'Mon-YY') AS purchase_month,
                              --Calculating net revenue (((total_bags * 30) - waste_pieces) * rate_per_piece)
                                        SUM(((total_bags * 30 )- waste_pieces)*rate_per_piece) AS monthly_purchase
                                   FROM finance.purchases
                                   WHERE
                                        purchase_date >= '2025-01-01' AND purchase_date <= '2025-12-31'
                                   GROUP BY
                                        seller_id,
                                        TO_CHAR(purchase_date, 'Mon-YY')
                              ),
                              --Using CASE WHEN statement with aggregation SUM to make PIVOT TABLE and GROUP BY seller_id to ensure unique row per seller.
                                   transform_data AS
                              (
                                   SELECT
                                        seller_id,
                                        SUM(CASE WHEN purchase_month = 'Jan-25' THEN monthly_purchase ELSE 0 END) AS Jan_25,
                                        SUM(CASE WHEN purchase_month = 'Feb-25' THEN monthly_purchase ELSE 0 END) AS Feb_25,
                                        SUM(CASE WHEN purchase_month = 'Mar-25' THEN monthly_purchase ELSE 0 END) AS Mar_25,
                                        SUM(CASE WHEN purchase_month = 'Apr-25' THEN monthly_purchase ELSE 0 END) AS Apr_25,
                                        SUM(CASE WHEN purchase_month = 'May-25' THEN monthly_purchase ELSE 0 END) AS May_25,
                                        SUM(CASE WHEN purchase_month = 'Jun-25' THEN monthly_purchase ELSE 0 END) AS Jun_25,
                                        SUM(CASE WHEN purchase_month = 'Jul-25' THEN monthly_purchase ELSE 0 END) AS Jul_25,
                                        SUM(CASE WHEN purchase_month = 'Aug-25' THEN monthly_purchase ELSE 0 END) AS Aug_25,
                                        SUM(CASE WHEN purchase_month = 'Sep-25' THEN monthly_purchase ELSE 0 END) AS Sep_25,
                                        SUM(CASE WHEN purchase_month = 'Oct-25' THEN monthly_purchase ELSE 0 END) AS Oct_25,
                                        SUM(CASE WHEN purchase_month = 'Nov-25' THEN monthly_purchase ELSE 0 END) AS Nov_25,
                                        SUM(CASE WHEN purchase_month = 'Dec-25' THEN monthly_purchase ELSE 0 END) AS Dec_25
                                   FROM extract_data 
                                   GROUP BY
                                        seller_id
                              ),

                              --Finding total yearly revenue per seller.

                                   load_data AS
                              (
                                   SELECT
                                        *,
                                        (Jan_25+Feb_25+Mar_25+Apr_25+May_25+Jun_25+Jul_25+Aug_25+Sep_25+Oct_25+Nov_25+Dec_25) AS yearly_total
                                   FROM transform_data

                              )

                              --Joining master.sellers to fetch seller_name for business readability.

                                   SELECT 
							  	s.seller_id,
                                        s.seller_name,
								s.is_active,
                                        COALESCE(ld.jan_25, 0) AS jan_25,
								COALESCE(ld.feb_25, 0) AS feb_25,
								COALESCE(ld.mar_25, 0) AS mar_25,
								COALESCE(ld.apr_25, 0) AS apr_25,
								COALESCE(ld.may_25, 0) AS may_25,
								COALESCE(ld.jun_25, 0) AS jun_25,
								COALESCE(ld.jul_25, 0) AS jul_25,
								COALESCE(ld.aug_25, 0) AS aug_25,
								COALESCE(ld.sep_25, 0) AS sep_25,
								COALESCE(ld.oct_25, 0) AS oct_25,
								COALESCE(ld.nov_25, 0) AS nov_25,
								COALESCE(ld.dec_25, 0) AS dec_25,
								COALESCE(ld.yearly_total, 0) AS yearly_total				   
                                   FROM master.sellers s
                                   LEFT JOIN load_data ld
                                   ON ld.seller_id = s.seller_id
							  ORDER BY
							  		s.seller_id;
                              '''
HIERARCHICAL_REVENUE_QUERY =  '''
                              WITH extract_data AS
                              (
                                   SELECT
                                        seller_id,

                              --Calculating net revenue per seller (((total_bags * 30) - waste_pieces) * rate_per_piece)

                                        SUM(((total_bags * 30) - waste_pieces) * rate_per_piece) AS total_amount

                                   FROM finance.purchases

                                   GROUP BY
                                        seller_id
                              )

                              SELECT
                                   s.seller_name,
                                   l.city,
                                   l.state,
                                   SUM(ed.total_amount) AS total_revenue,

                              --GROUPING() is used here to differentiate genuine NULL or generated by Subtotal"
                              --GROUPING() = 0(this column is used while grouping)
                              --GROUPING() = 1(NULL generated by subtotal and this column is ignored while grouping)

                                   GROUPING(s.seller_name)  AS grouping_seller_name,
                                   GROUPING(l.city)		AS grouping_city,
                                   GROUPING(l.state)		AS grouping_state

                              FROM extract_data ed
                              INNER JOIN master.sellers s
                                   ON ed.seller_id = s.seller_id
                              INNER JOIN master.locations l
                                   ON s.address_id = l.address_id

                              --ROLLUP() does hierarchical aggregation, top to down

                              GROUP BY ROLLUP(l.state,l.city,s.seller_name)

                              ORDER BY
                                   l.state        ASC,
                                   l.city	     ASC,
                                   s.seller_name	ASC;
                             '''