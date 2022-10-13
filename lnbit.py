
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import requests

ln_withdraw = "https://legend.lnbits.com/withdraw/api/v1/links"

class LNbits():

    html = '''<!DOCTYPE html>

<html lang="en">

<head>

	<link rel="stylesheet" type="text/css" href="/static/vendor/quasar@1.13.2/quasar.min.css" />

	<link rel="stylesheet" type="text/css" href="/static/vendor/vue-qrcode-reader@2.2.0/vue-qrcode-reader.min.css" />

	<link rel="stylesheet" type="text/css" href="/static/vendor/chart.js@2.9.3/chart.min.css" />

	<!---->
	<link rel="stylesheet" type="text/css" href="/static/css/base.css" />

	<title> Test - LNbits </title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, shrink-to-fit=no" />
	<meta name="mobile-web-app-capable" content="yes" />
	<meta name="apple-mobile-web-app-capable" content="yes" />

	<link async="async" rel="manifest" href="/manifest/80cdc0dc33504fb8a3233930b0ab12c1.webmanifest" />

</head>

<body data-theme="bitcoin">
	<q-layout id="vue" view="hHh lpR lfr" v-cloak>
		<q-header bordered class="bg-marginal-bg">
			<q-toolbar>

				<q-btn dense flat round icon="menu" @click="g.visibleDrawer = !g.visibleDrawer"></q-btn>

				<q-toolbar-title>
					<q-btn flat no-caps dense size="lg" type="a" href="/">

						<span><strong>LN</strong>bits</span>
					</q-btn>
				</q-toolbar-title>

				<q-badge color="yellow" text-color="black" class="q-mr-md">
					<span
              ><span v-show="$q.screen.gt.sm"
                >USE WITH CAUTION - LNbits wallet is still in </span>BETA</span>
				</q-badge>

				<q-badge v-if="g.offline" color="red" text-color="white" class="q-mr-md">
					<span> OFFLINE </span>
				</q-badge>
				<q-btn-dropdown v-if="g.allowedThemes && g.allowedThemes.length > 1" dense flat round size="sm"
					icon="dashboard_customize" class="q-pl-md">
					<div class="row no-wrap q-pa-md">
						<q-btn v-if="g.allowedThemes.includes('classic')" dense flat @click="changeColor('classic')"
							icon="format_color_fill" color="deep-purple" size="md">
							<q-tooltip>classic</q-tooltip>
						</q-btn>
						<q-btn v-if="g.allowedThemes.includes('bitcoin')" dense flat @click="changeColor('bitcoin')"
							icon="format_color_fill" color="orange" size="md">
							<q-tooltip>bitcoin</q-tooltip>
						</q-btn>
						<q-btn v-if="g.allowedThemes.includes('mint')" dense flat @click="changeColor('mint')"
							icon="format_color_fill" color="green" size="md">
							<q-tooltip>mint</q-tooltip>
						</q-btn>
						<q-btn v-if="g.allowedThemes.includes('autumn')" dense flat @click="changeColor('autumn')"
							icon="format_color_fill" color="brown" size="md">
							<q-tooltip>autumn</q-tooltip>
						</q-btn>
						<q-btn v-if="g.allowedThemes.includes('monochrome')" dense flat
							@click="changeColor('monochrome')" icon="format_color_fill" color="grey" size="md">
							<q-tooltip>monochrome</q-tooltip>
						</q-btn>
						<q-btn v-if="g.allowedThemes.includes('salvador')" dense flat @click="changeColor('salvador')"
							icon="format_color_fill" color="blue-10" size="md">
							<q-tooltip>elSalvador</q-tooltip>
						</q-btn>
						<q-btn v-if="g.allowedThemes.includes('freedom')" dense flat @click="changeColor('freedom')"
							icon="format_color_fill" color="pink-13" size="md">
							<q-tooltip>Freedom</q-tooltip>
						</q-btn>
						<q-btn v-if="g.allowedThemes.includes('flamingo')" dense flat @click="changeColor('flamingo')"
							icon="format_color_fill" color="pink-3" size="md">
							<q-tooltip>flamingo</q-tooltip>
						</q-btn>
					</div>
				</q-btn-dropdown>

				<q-btn dense flat round @click="toggleDarkMode" :icon="($q.dark.isActive) ? 'brightness_3' : 'wb_sunny'"
					size="sm">
					<q-tooltip>Toggle Dark Mode</q-tooltip>
				</q-btn>
			</q-toolbar>
		</q-header>


		<q-drawer v-model="g.visibleDrawer" side="left" :width="($q.screen.lt.md) ? 260 : 230" show-if-above
			:elevated="$q.screen.lt.md">
			<lnbits-wallet-list></lnbits-wallet-list>
			<lnbits-extension-list class="q-pb-xl"></lnbits-extension-list>
		</q-drawer>

		<q-page-container>
			<q-page class="q-px-md q-py-lg" :class="{'q-px-lg': $q.screen.gt.xs}">

				<div class="row q-col-gutter-md">
					<div class="col-12 col-md-7 q-gutter-y-md">
						<q-card>
							<q-card-section>
								<h3 class="q-my-none">
									<strong>{{ formattedBalance }} </strong>
									sats
									<q-btn v-if="'False' == 'True'" flat round color="primary" icon="add" size="md">
										<q-popup-edit class="bg-accent text-white" v-slot="scope" v-model="credit">
											<q-input v-if="'sats' != 'sats'" label="Amount to credit account"
												v-model="scope.value" dense autofocus mask="#.##" fill-mask="0"
												reverse-fill-mask @keyup.enter="updateBalance(scope.value)">
												<template v-slot:append>
													<q-icon name="edit" />
												</template>
											</q-input>
											<q-input v-else type="number" label="Amount to credit account"
												v-model="scope.value" dense autofocus
												@keyup.enter="updateBalance(scope.value)">
												<template v-slot:append>
													<q-icon name="edit" />
												</template>
											</q-input>
										</q-popup-edit>
									</q-btn>
								</h3>
							</q-card-section>
							<div class="row q-pb-md q-px-md q-col-gutter-md gt-sm">
								<div class="col">
									<q-btn unelevated color="primary" class="full-width" @click="showParseDialog">Paste
										Request</q-btn>
								</div>
								<div class="col">
									<q-btn unelevated color="primary" class="full-width" @click="showReceiveDialog">
										Create Invoice</q-btn>
								</div>
								<div class="col">
									<q-btn unelevated color="secondary" icon="photo_camera" @click="showCamera">scan
										<q-tooltip>Use camera to scan an invoice/QR</q-tooltip>
									</q-btn>
								</div>
							</div>
						</q-card>

						<q-card>
							<q-card-section>
								<div class="row items-center no-wrap q-mb-sm">
									<div class="col">
										<h5 class="text-subtitle1 q-my-none">Transactions</h5>
									</div>
									<div class="col-auto">
										<q-btn flat color="grey" @click="exportCSV">Export to CSV</q-btn>
										<!--<q-btn v-if="pendingPaymentsExist" dense flat round icon="update" color="grey" @click="checkPendingPayments">
                <q-tooltip>Check pending</q-tooltip>
              </q-btn>-->
										<q-btn dense flat round icon="show_chart" color="grey" @click="showChart">
											<q-tooltip>Show chart</q-tooltip>
										</q-btn>
									</div>
								</div>
								<q-input v-if="payments.length > 10" filled dense clearable
									v-model="paymentsTable.filter" debounce="300"
									placeholder="Search by tag, memo, amount" class="q-mb-md">
								</q-input>
								<q-table dense flat :data="filteredPayments" :row-key="paymentTableRowKey"
									:columns="paymentsTable.columns" :pagination.sync="paymentsTable.pagination"
									no-data-label="No transactions made yet" :filter="paymentsTable.filter">

									<template v-slot:header="props">
										<q-tr :props="props">
											<q-th auto-width></q-th>
											<q-th v-for="col in props.cols" :key="col.name" :props="props">
												{{ col.label }}</q-th>
										</q-tr>
									</template>
									<template v-slot:body="props">
										<q-tr :props="props">
											<q-td auto-width class="text-center">
												<q-icon v-if="props.row.isPaid" size="14px"
													:name="props.row.isOut ? 'call_made' : 'call_received'"
													:color="props.row.isOut ? 'pink' : 'green'"
													@click="props.expand = !props.expand"></q-icon>
												<q-icon v-else name="settings_ethernet" color="grey"
													@click="props.expand = !props.expand">
													<q-tooltip>Pending</q-tooltip>
												</q-icon>
											</q-td>
											<q-td key="memo" :props="props"
												style="white-space: normal; word-break: break-all">
												<q-badge v-if="props.row.tag" color="yellow" text-color="black">
													<a class="inherit"
														:href="['/', props.row.tag, '/?usr=', user.id].join('')">
														#{{ props.row.tag }}
													</a>
												</q-badge>
												{{ props.row.memo }}
											</q-td>
											<q-td auto-width key="date" :props="props">
												<q-tooltip>{{ props.row.date }}</q-tooltip>
												{{ props.row.dateFrom }}
											</q-td>

											<q-td auto-width key="sat" v-if="'sats' != 'sats'" :props="props"> {{ parseFloat(String(props.row.fsat).replaceAll(",",
                "")) / 100 }}
											</q-td>

											<q-td auto-width key="sat" v-else :props="props">
												{{ props.row.fsat }}
											</q-td>
											<q-td auto-width key="fee" :props="props">
												{{ props.row.fee }}
											</q-td>
										</q-tr>

										<q-dialog v-model="props.expand" :props="props">
											<q-card class="q-pa-lg q-pt-xl lnbits__dialog-card">
												<div class="text-center q-mb-lg">
													<div v-if="props.row.isIn && props.row.pending">
														<q-icon name="settings_ethernet" color="grey"></q-icon>
														Invoice waiting to be paid
														<lnbits-payment-details :payment="props.row">
														</lnbits-payment-details>
														<div v-if="props.row.bolt11" class="text-center q-mb-lg">
															<a :href="'lightning:' + props.row.bolt11">
																<q-responsive :ratio="1" class="q-mx-xl">
																	<qrcode :value="props.row.bolt11"
																		:options="{width: 340}" class="rounded-borders">
																	</qrcode>
																</q-responsive>
															</a>
														</div>
														<div class="row q-mt-lg">
															<q-btn outline color="grey"
																@click="copyText(props.row.bolt11)">Copy invoice</q-btn>
															<q-btn v-close-popup flat color="grey" class="q-ml-auto">
																Close</q-btn>
														</div>
													</div>
													<div v-else-if="props.row.isPaid && props.row.isIn">
														<q-icon size="18px" :name="'call_received'" :color="'green'">
														</q-icon>
														Payment Received
														<lnbits-payment-details :payment="props.row">
														</lnbits-payment-details>
													</div>
													<div v-else-if="props.row.isPaid && props.row.isOut">
														<q-icon size="18px" :name="'call_made'" :color="'pink'">
														</q-icon>
														Payment Sent
														<lnbits-payment-details :payment="props.row">
														</lnbits-payment-details>
													</div>
													<div v-else-if="props.row.isOut && props.row.pending">
														<q-icon name="settings_ethernet" color="grey"></q-icon>
														Outgoing payment pending
														<lnbits-payment-details :payment="props.row">
														</lnbits-payment-details>
													</div>
												</div>
											</q-card>
										</q-dialog>
									</template>

								</q-table>
							</q-card-section>
						</q-card>
					</div>


					<div class="col-12 col-md-5 q-gutter-y-md">
						<q-card>
							<q-card-section>
								<h6 class="text-subtitle1 q-mt-none q-mb-sm">
									LNbits Wallet: <strong><em>Test</em></strong>
								</h6>
							</q-card-section>
							<q-card-section class="q-pa-none">
								<q-separator></q-separator>

								<q-list>
									<q-expansion-item group="extras" icon="swap_vertical_circle" label="API info"
										:content-inset-level="0.5">
										<q-card-section>
											<strong>Wallet ID: </strong><em>fa84543560b4462eb8182f13054bc317</em><br />
											<strong>Admin key: </strong><em>9aba4d73ed4946b3a43c532629da3a42</em><br />
											<strong>Invoice/read key: </strong><em>a808acba300544bb8922411166f390da</em>
										</q-card-section>
										<q-expansion-item group="api" dense expand-separator label="Get wallet details">
											<q-card>
												<q-card-section>
													<code><span class="text-light-green">GET</span> /api/v1/wallet</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Headers</h5>
													<code>{"X-Api-Key": "<i>a808acba300544bb8922411166f390da</i>"}</code><br />
													<h5 class="text-caption q-mt-sm q-mb-none">
														Returns 200 OK (application/json)
													</h5>
													<code
          >{"id": &lt;string&gt;, "name": &lt;string&gt;, "balance":
          &lt;int&gt;}</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Curl example</h5>
													<code
          >curl https://legend.lnbits.com/api/v1/wallet -H "X-Api-Key:
          <i>a808acba300544bb8922411166f390da</i>"</code>
												</q-card-section>
											</q-card>
										</q-expansion-item>
										<q-expansion-item group="api" dense expand-separator
											label="Create an invoice (incoming)">
											<q-card>
												<q-card-section>
													<code><span class="text-light-green">POST</span> /api/v1/payments</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Headers</h5>
													<code>{"X-Api-Key": "<i>a808acba300544bb8922411166f390da</i>"}</code><br />
													<h5 class="text-caption q-mt-sm q-mb-none">Body (application/json)
													</h5>
													<code
          >{"out": false, "amount": &lt;int&gt;, "memo": &lt;string&gt;, "unit":
          &lt;string&gt;, "webhook": &lt;url:string&gt;, "internal":
          &lt;bool&gt;}</code>
													<h5 class="text-caption q-mt-sm q-mb-none">
														Returns 201 CREATED (application/json)
													</h5>
													<code
          >{"payment_hash": &lt;string&gt;, "payment_request":
          &lt;string&gt;}</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Curl example</h5>
													<code
          >curl -X POST https://legend.lnbits.com/api/v1/payments -d '{"out": false,
          "amount": &lt;int&gt;, "memo": &lt;string&gt;, "webhook":
          &lt;url:string&gt;, "unit": &lt;string&gt;}' -H "X-Api-Key:
          <i>a808acba300544bb8922411166f390da</i>" -H "Content-type: application/json"</code>
												</q-card-section>
											</q-card>
										</q-expansion-item>
										<q-expansion-item group="api" dense expand-separator
											label="Pay an invoice (outgoing)">
											<q-card>
												<q-card-section>
													<code><span class="text-light-green">POST</span> /api/v1/payments</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Headers</h5>
													<code>{"X-Api-Key": "9aba4d73ed4946b3a43c532629da3a42"}</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Body (application/json)
													</h5>
													<code>{"out": true, "bolt11": &lt;string&gt;}</code>
													<h5 class="text-caption q-mt-sm q-mb-none">
														Returns 201 CREATED (application/json)
													</h5>
													<code>{"payment_hash": &lt;string&gt;}</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Curl example</h5>
													<code
          >curl -X POST https://legend.lnbits.com/api/v1/payments -d '{"out": true,
          "bolt11": &lt;string&gt;}' -H "X-Api-Key:
          <i>9aba4d73ed4946b3a43c532629da3a42"</i> -H "Content-type:
          application/json"</code>
												</q-card-section>
											</q-card>
										</q-expansion-item>

										<q-expansion-item group="api" dense expand-separator label="Decode an invoice">
											<q-card>
												<q-card-section>
													<code
          ><span class="text-light-green">POST</span>
          /api/v1/payments/decode</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Headers</h5>
													<code>{"X-Api-Key": "<i>a808acba300544bb8922411166f390da</i>"}</code><br />
													<h5 class="text-caption q-mt-sm q-mb-none">Body (application/json)
													</h5>
													<code>{"invoice": &lt;string&gt;}</code>
													<h5 class="text-caption q-mt-sm q-mb-none">
														Returns 200 (application/json)
													</h5>
													<h5 class="text-caption q-mt-sm q-mb-none">Curl example</h5>
													<code
          >curl -X POST https://legend.lnbits.com/api/v1/payments/decode -d
          '{"data": &lt;bolt11/lnurl, string&gt;}' -H "X-Api-Key:
          <i>a808acba300544bb8922411166f390da</i>" -H "Content-type: application/json"</code>
												</q-card-section>
											</q-card>
										</q-expansion-item>
										<q-expansion-item group="api" dense expand-separator
											label="Check an invoice (incoming or outgoing)" class="q-pb-md">
											<q-card>
												<q-card-section>
													<code
          ><span class="text-light-blue">GET</span>
          /api/v1/payments/&lt;payment_hash&gt;</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Headers</h5>
													<code>{"X-Api-Key": "a808acba300544bb8922411166f390da"}</code>
													<h5 class="text-caption q-mt-sm q-mb-none">
														Returns 200 OK (application/json)
													</h5>
													<code>{"paid": &lt;bool&gt;}</code>
													<h5 class="text-caption q-mt-sm q-mb-none">Curl example</h5>
													<code
          >curl -X GET https://legend.lnbits.com/api/v1/payments/&lt;payment_hash&gt; -H "X-Api-Key:
          <i>a808acba300544bb8922411166f390da"</i> -H "Content-type: application/json"</code>
												</q-card-section>
											</q-card>
										</q-expansion-item>
									</q-expansion-item>
									<q-separator></q-separator>



									<q-expansion-item group="extras" icon="settings_cell"
										label="Export to Phone with QR Code">
										<q-card>
											<q-card-section class="text-center">
												<p>
													This QR code contains your wallet URL with full access. You
													can scan it from your phone to open your wallet from there.
												</p>
												<qrcode
													:value="'https://legend.lnbits.com/' +'wallet?usr=80cdc0dc33504fb8a3233930b0ab12c1&wal=fa84543560b4462eb8182f13054bc317'"
													:options="{width:240}"></qrcode>
											</q-card-section>
										</q-card>
									</q-expansion-item>
									<q-separator></q-separator>
									<q-expansion-item group="extras" icon="edit" label="Rename wallet">
										<q-card>
											<q-card-section>
												<div class="" style="max-width: 320px">
													<q-input filled v-model.trim="newName" label="Label" dense="dense"
														@update:model-value="(e) => console.log(e)" />
												</div>
												<q-btn :disable="!newName.length" unelevated class="q-mt-sm"
													color="primary" @click="updateWalletName()">Update name</q-btn>
											</q-card-section>
										</q-card>
									</q-expansion-item>
									<q-separator></q-separator>
									<q-expansion-item group="extras" icon="remove_circle" label="Delete wallet">
										<q-card>
											<q-card-section>
												<p>
													This whole wallet will be deleted, the funds will be
													<strong>UNRECOVERABLE</strong>.
												</p>
												<q-btn unelevated color="red-10"
													@click="deleteWallet('fa84543560b4462eb8182f13054bc317', '80cdc0dc33504fb8a3233930b0ab12c1')">
													Delete wallet</q-btn>
											</q-card-section>
										</q-card>
									</q-expansion-item>
								</q-list>
							</q-card-section>
						</q-card>

					</div>
				</div>

				<q-dialog v-model="receive.show" @hide="closeReceiveDialog">

					<q-card v-if="!receive.paymentReq" class="q-pa-lg q-pt-xl lnbits__dialog-card">
						<q-form @submit="createInvoice" class="q-gutter-md">
							<p v-if="receive.lnurl" class="text-h6 text-center q-my-none">
								<b>{{receive.lnurl.domain}}</b> is requesting an invoice:
							</p>

							<q-select filled dense v-model="receive.unit" type="text" label="Unit"
								:options="receive.units"></q-select>
							<q-input ref="setAmount" filled dense v-model.number="receive.data.amount"
								:label="'Amount (' + receive.unit + ') *'" :mask="receive.unit != 'sat' ? '#.##' : '#'"
								fill-mask="0" reverse-fill-mask :step="receive.unit != 'sat' ? '0.01' : '1'"
								:min="receive.minMax[0]" :max="receive.minMax[1]"
								:readonly="receive.lnurl && receive.lnurl.fixed"></q-input>


							<q-input filled dense v-model.trim="receive.data.memo" label="Memo"></q-input>

							<div v-if="receive.status == 'pending'" class="row q-mt-lg">
								<q-btn unelevated color="primary"
									:disable="receive.data.amount == null || receive.data.amount <= 0" type="submit">
									<span v-if="receive.lnurl">
              Withdraw from {{receive.lnurl.domain}}
            </span>
									<span v-else> Create invoice </span>
								</q-btn>
								<q-btn v-close-popup flat color="grey" class="q-ml-auto">Cancel</q-btn>
							</div>
							<q-spinner v-if="receive.status == 'loading'" color="primary" size="2.55em"></q-spinner>
						</q-form>
					</q-card>
					<q-card v-else class="q-pa-lg q-pt-xl lnbits__dialog-card">
						<div class="text-center q-mb-lg">
							<a :href="'lightning:' + receive.paymentReq">
								<q-responsive :ratio="1" class="q-mx-xl">
									<qrcode :value="receive.paymentReq" :options="{width: 340}" class="rounded-borders">
									</qrcode>
								</q-responsive>
							</a>
						</div>
						<div class="row q-mt-lg">
							<q-btn outline color="grey" @click="copyText(receive.paymentReq)">Copy invoice</q-btn>
							<q-btn v-close-popup flat color="grey" class="q-ml-auto">Close</q-btn>
						</div>
					</q-card>

				</q-dialog>

				<q-dialog v-model="parse.show" @hide="closeParseDialog">
					<q-card class="q-pa-lg q-pt-xl lnbits__dialog-card">
						<div v-if="parse.invoice">
							<h6 v-if="'sats' != 'sats'" class="q-my-none">
								{{ parseFloat(String(parse.invoice.fsat).replaceAll(",",
          "")) / 100 }} sats
							</h6>
							<h6 v-else class="q-my-none">
								{{ parse.invoice.fsat }} sats
							</h6>
							<q-separator class="q-my-sm"></q-separator>
							<p class="text-wrap">
								<strong>Description:</strong> {{ parse.invoice.description }}<br />
								<strong>Expire date:</strong> {{ parse.invoice.expireDate }}<br />
								<strong>Hash:</strong> {{ parse.invoice.hash }}
							</p>

							<div v-if="canPay" class="row q-mt-lg">
								<q-btn unelevated color="primary" @click="payInvoice">Pay</q-btn>
								<q-btn v-close-popup flat color="grey" class="q-ml-auto">Cancel</q-btn>
							</div>
							<div v-else class="row q-mt-lg">
								<q-btn unelevated disabled color="yellow" text-color="black">Not enough funds!</q-btn>
								<q-btn v-close-popup flat color="grey" class="q-ml-auto">Cancel</q-btn>
							</div>
						</div>
						<div v-else-if="parse.lnurlauth">

							<q-form @submit="authLnurl" class="q-gutter-md">
								<p class="q-my-none text-h6">
									Authenticate with <b>{{ parse.lnurlauth.domain }}</b>?
								</p>
								<q-separator class="q-my-sm"></q-separator>
								<p>
									For every website and for every LNbits wallet, a new keypair will be
									deterministically generated so your identity can't be tied to your
									LNbits wallet or linked across websites. No other data will be
									shared with {{ parse.lnurlauth.domain }}.
								</p>
								<p>Your public key for <b>{{ parse.lnurlauth.domain }}</b> is:</p>
								<p class="q-mx-xl">
									<code class="text-wrap"> {{ parse.lnurlauth.pubkey }} </code>
								</p>
								<div class="row q-mt-lg">
									<q-btn unelevated color="primary" type="submit">Login</q-btn>
									<q-btn v-close-popup flat color="grey" class="q-ml-auto">Cancel</q-btn>
								</div>
							</q-form>

						</div>
						<div v-else-if="parse.lnurlpay">

							<q-form @submit="payLnurl" class="q-gutter-md">
								<p v-if="parse.lnurlpay.fixed" class="q-my-none text-h6">
									<b>{{ parse.lnurlpay.domain }}</b> is requesting {{
            parse.lnurlpay.maxSendable | msatoshiFormat }}
									{{LNBITS_DENOMINATION}}
									<span v-if="parse.lnurlpay.commentAllowed > 0">
              <br />
              and a {{parse.lnurlpay.commentAllowed}}-char comment
            </span>
								</p>
								<p v-else class="q-my-none text-h6 text-center">
									<b>{{ parse.lnurlpay.targetUser || parse.lnurlpay.domain }}</b> is
									requesting <br />
            between <b>{{ parse.lnurlpay.minSendable | msatoshiFormat }}</b> and
									<b>{{ parse.lnurlpay.maxSendable | msatoshiFormat }}</b>
									sats
									<span v-if="parse.lnurlpay.commentAllowed > 0">
              <br />
              and a {{parse.lnurlpay.commentAllowed}}-char comment
            </span>
								</p>
								<q-separator class="q-my-sm"></q-separator>
								<div class="row">
									<p class="col text-justify text-italic">
										{{ parse.lnurlpay.description }}
									</p>
									<p class="col-4 q-pl-md" v-if="parse.lnurlpay.image">
										<q-img :src="parse.lnurlpay.image" />
									</p>
								</div>
								<div class="row">
									<div class="col">

										<q-input filled dense v-model.number="parse.data.amount" type="number"
											label="Amount (sats) *" :min="parse.lnurlpay.minSendable / 1000"
											:max="parse.lnurlpay.maxSendable / 1000" :readonly="parse.lnurlpay.fixed">
										</q-input>

									</div>
									<div class="col-8 q-pl-md" v-if="parse.lnurlpay.commentAllowed > 0">
										<q-input filled dense v-model="parse.data.comment"
											:type="parse.lnurlpay.commentAllowed > 64 ? 'textarea' : 'text'"
											label="Comment (optional)" :maxlength="parse.lnurlpay.commentAllowed">
										</q-input>
									</div>
								</div>
								<div class="row q-mt-lg">
									<q-btn unelevated color="primary" type="submit">Send {{LNBITS_DENOMINATION}}</q-btn>
									<q-btn v-close-popup flat color="grey" class="q-ml-auto">Cancel</q-btn>
								</div>
							</q-form>

						</div>
						<div v-else>
							<q-form v-if="!parse.camera.show" @submit="decodeRequest" class="q-gutter-md">
								<q-input filled dense v-model.trim="parse.data.request" type="textarea"
									label="Paste an invoice, payment request or lnurl code *">
								</q-input>
								<div class="row q-mt-lg">
									<q-btn unelevated color="primary" :disable="parse.data.request == ''" type="submit">
										Read</q-btn>
									<q-btn v-close-popup flat color="grey" class="q-ml-auto">Cancel</q-btn>
								</div>
							</q-form>
							<div v-else>
								<q-responsive :ratio="1">
									<qrcode-stream @decode="decodeQR" class="rounded-borders"></qrcode-stream>
								</q-responsive>
								<div class="row q-mt-lg">
									<q-btn @click="closeCamera" flat color="grey" class="q-ml-auto">
										Cancel
									</q-btn>
								</div>
							</div>
						</div>
					</q-card>
				</q-dialog>

				<q-dialog v-model="parse.camera.show">
					<q-card class="q-pa-lg q-pt-xl">
						<div class="text-center q-mb-lg">
							<qrcode-stream @decode="decodeQR" class="rounded-borders"></qrcode-stream>
						</div>
						<div class="row q-mt-lg">
							<q-btn @click="closeCamera" flat color="grey" class="q-ml-auto">Cancel</q-btn>
						</div>
					</q-card>
				</q-dialog>

				<q-dialog v-model="paymentsChart.show">
					<q-card class="q-pa-sm" style="width: 800px; max-width: unset">
						<q-card-section>
							<canvas ref="canvas" width="600" height="400"></canvas>
						</q-card-section>
					</q-card>
				</q-dialog>
				<q-tabs class="lt-md fixed-bottom left-0 right-0 bg-primary text-white shadow-2 z-top"
					active-class="px-0" indicator-color="transparent">
					<q-tab icon="account_balance_wallet" label="Wallets" @click="g.visibleDrawer = !g.visibleDrawer">
					</q-tab>
					<q-tab icon="content_paste" label="Paste" @click="showParseDialog"> </q-tab>
					<q-tab icon="file_download" label="Receive" @click="showReceiveDialog">
					</q-tab>

					<q-tab icon="photo_camera" label="Scan" @click="showCamera"> </q-tab>
				</q-tabs>

				<q-dialog v-model="disclaimerDialog.show">
					<q-card class="q-pa-lg">
						<h6 class="q-my-md text-primary">Warning</h6>
						<p>
							Login functionality to be released in a future update, for now,
							<strong
          >make sure you bookmark this page for future access to your
          wallet</strong>!
						</p>
						<p>
							This service is in BETA, and we hold no responsibility for people losing
							access to funds.
						</p>
						<div class="row q-mt-lg">
							<q-btn outline color="grey" @click="copyText(disclaimerDialog.location.href)">Copy wallet
								URL</q-btn>
							<q-btn v-close-popup flat color="grey" class="q-ml-auto">I understand</q-btn>
						</div>
					</q-card>
				</q-dialog>

			</q-page>
		</q-page-container>


		<q-footer class="bg-transparent q-px-lg q-py-md" :class="{'text-dark': !$q.dark.isActive}">
			<q-toolbar class="gt-sm">
				<q-toolbar-title class="text-caption">
					LNbits, free and open-source lightning wallet
					<br />

					<small v-if="'LNbits' == 'LNbits'"
              >Commit version: d1302e4868f0fe12cf6bdf7d25e82045981077c2</small>
				</q-toolbar-title>
				<q-space></q-space>
				<q-btn flat dense :color="($q.dark.isActive) ? 'white' : 'primary'" icon="code" type="a"
					href="https://github.com/lnbits/lnbits" target="_blank" rel="noopener">
					<q-tooltip>View project in GitHub</q-tooltip>
				</q-btn>
			</q-toolbar>
		</q-footer>


	</q-layout>


	<!---->

	<script src="/static/vendor/moment@2.27.0/moment.min.js"></script>

	<script src="/static/vendor/vue@2.6.12/vue.js"></script>

	<script src="/static/vendor/vue-router@3.4.3/vue-router.js"></script>

	<script src="/static/vendor/quasar@1.13.2/quasar.ie.polyfills.umd.min.js"></script>

	<script src="/static/vendor/axios@0.20.0/axios.min.js"></script>

	<script src="/static/vendor/bolt11/decoder.js"></script>

	<script src="/static/vendor/chart.js@2.9.3/chart.min.js"></script>

	<script src="/static/vendor/quasar@1.13.2/quasar.umd.js"></script>

	<script src="/static/vendor/underscore@1.10.2/underscore.min.js"></script>

	<script src="/static/vendor/vue-qrcode-reader@2.2.0/vue-qrcode-reader.min.js"></script>

	<script src="/static/vendor/vue-qrcode@1.0.2/vue-qrcode.min.js"></script>

	<script src="/static/vendor/vuex@3.5.1/vuex.js"></script>

	<!---->
	<script src="/static/js/base.js"></script>
	<script src="/static/js/components.js"></script>
	<script type="text/javascript">
		const themes = ["bitcoin", "mint", "freedom", "classic", "autumn", "monochrome", "salvador"]
      const LNBITS_DENOMINATION = "sats"
      if(themes && themes.length) {
        window.allowedThemes = themes.map(str => str.trim())
      }
	</script>
	<script>
		window.extensions = [["boltz", true, false, "Boltz", "Perform onchain/offchain swaps", "swap_horiz", ["dni"], false], ["satsdice", true, false, "Sats Dice", "LNURL Satoshi dice", "casino", ["arcbtc"], false], ["withdraw", true, false, "LNURLw", "Make LNURL withdraw links", "crop_free", ["arcbtc", "eillarra"], false], ["jukebox", true, false, "Spotify Jukebox", "Spotify jukebox middleware", "radio", ["benarc"], false], ["scrub", true, false, "Scrub", "Pass payments to LNURLp/LNaddress", "send", ["arcbtc", "talvasconcelos"], false], ["boltcards", true, false, "Bolt Cards", "Self custody Bolt Cards with one time LNURLw", "payment", ["iwarpbtc", "arcbtc", "leesalminen"], false], ["streamalerts", true, false, "Stream Alerts", "Bitcoin donations in stream alerts", "notifications_active", ["Fittiboy"], false], ["splitpayments", true, false, "Split Payments", "Split incoming payments across wallets", "call_split", ["fiatjaf", "cryptograffiti"], false], ["bleskomat", true, false, "Bleskomat", "Connect a Bleskomat ATM to an lnbits", "money", ["chill117"], false], ["paywall", true, false, "Paywall", "Create paywalls for content", "policy", ["eillarra"], false], ["invoices", true, false, "Invoices", "Create invoices for your clients.", "request_quote", ["leesalminen"], false], ["hivemind", true, false, "Hivemind", "Make cheap talk expensive!", "batch_prediction", ["fiatjaf"], false], ["tipjar", true, false, "Tip Jar", "Accept Bitcoin donations, with messages attached!", "favorite", ["Fittiboy"], false], ["copilot", true, false, "Streamer Copilot", "Video tips/animations/webhooks", "face", ["arcbtc"], false], ["livestream", true, false, "DJ Livestream", "Sell tracks and split revenue (lnurl-pay)", "speaker", ["fiatjaf", "cryptograffiti"], false], ["lnurldevice", true, false, "LNURLDevice", "For offline LNURL devices", "point_of_sale", ["arcbtc"], false], ["usermanager", true, false, "User Manager", "Generate users and wallets", "person_add", ["benarc"], false], ["subdomains", true, false, "Subdomains", "Sell subdomains of your domain", "domain", ["grmkris"], false], ["tpos", true, false, "TPoS", "A shareable PoS terminal!", "dialpad", ["talvasconcelos", "arcbtc", "leesalminen"], false], ["lnaddress", true, false, "Lightning Address", "Sell LN addresses for your domain", "alternate_email", ["talvasconcelos"], false], ["offlineshop", true, false, "OfflineShop", "Receive payments for products offline!", "nature_people", ["fiatjaf"], false], ["lnurlp", true, false, "LNURLp", "Make reusable LNURL pay links", "receipt", ["arcbtc", "eillarra", "fiatjaf"], false], ["events", true, false, "Events", "Sell and register event tickets", "local_activity", ["benarc"], false], ["watchonly", true, false, "Onchain Wallet", "Onchain watch only wallets", "visibility", ["arcbtc", "motorina0"], false], ["lndhub", true, false, "LndHub", "Access lnbits from BlueWallet or Zeus", "navigation", ["fiatjaf"], false], ["discordbot", true, false, "Discord Bot", "Generate users and wallets", "person_add", ["bitcoingamer21"], false], ["satspay", true, false, "SatsPay Server", "Create onchain and LN charges", "payment", ["arcbtc"], false], ["lnticket", true, false, "Support Tickets", "LN support ticket system", "contact_support", ["benarc"], false]];
    
      window.user = {"admin": false, "email": null, "extensions": [], "id": "80cdc0dc33504fb8a3233930b0ab12c1", "password": null, "wallets": [{"adminkey": "9aba4d73ed4946b3a43c532629da3a42", "balance_msat": 0, "id": "fa84543560b4462eb8182f13054bc317", "inkey": "a808acba300544bb8922411166f390da", "name": "Test", "user": "80cdc0dc33504fb8a3233930b0ab12c1"}]};
    
    
      window.wallet = {"adminkey": "9aba4d73ed4946b3a43c532629da3a42", "balance_msat": 0, "id": "fa84543560b4462eb8182f13054bc317", "inkey": "a808acba300544bb8922411166f390da", "name": "Test", "user": "80cdc0dc33504fb8a3233930b0ab12c1"};
    
	</script>
	<script src="/core/static/js/wallet.js"></script>

</body>

</html>'''

    def page_parser(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        q_card_section = soup.find('q-card-section', attrs = {'class':'text-center'})
        qrcode = q_card_section.find('qrcode')
        ln_url = qrcode.attrs[':value'].replace("'", "").replace("+", "").replace(" ", "")
        parse_result = urlparse(ln_url)
        dict_parse_result = parse_qs(parse_result.query)
        user = dict_parse_result["usr"][0]
        wallet_id = dict_parse_result["wal"][0]
        return {user: user, wallet_id: wallet_id}

    def get_new_wallet_url(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        q_card_section = soup.find('q-card-section', attrs = {'class':'text-center'})
        qrcode = q_card_section.find('qrcode')
        ln_url = qrcode.attrs[':value'].replace("'", "").replace("+", "").replace(" ", "")
        return ln_url

    def create_withdrawal(self, ln_api_key):
        headers = {"Content-Type": "application/json", "X-Api-Key": ln_api_key}
        payload = {
            "title": "LN GiveAway",
            "min_withdrawable": 2,
            "max_withdrawable": 3,
            "uses": 1,
            "wait_time": 600000,
            "is_unique": True
        }
        response = requests.post(ln_withdraw, data=payload, headers=headers)
        if (response.status_code == 204):
            print(">>>> ", response.json())
            print(">>>> ", response.__dict__['raw'].__dict__)
        else:
            print("Error Creating Withdrawal")



